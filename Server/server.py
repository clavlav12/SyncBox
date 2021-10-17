"""
This server syncs all groups media players.
Group code is a string of 10 random numbers

protocol:
    Requests:  (client to server)
        - create_group_requests
        - start_video_request
        - join_group_request
        - start_video_vote_accept
        - start_video_vote_deny
        - pause_request
        - play_request
        - seek_request
        - stop_request
        - get_tick_rate
        - disconnect
        - send_message
        - get_time

    Responses: (server to client)
        - created
        - creation_failed
        - joined
        - group_not_found
        - start_video_vote_started
        - start_video_failed
        - start_video_succeeded
        - pause
        - play
        - seek
        - stop
        - tick_rate
        - message_received
        - users_list
        - late_start


all packets have a "send_time" parameter which states to when the packets was sent by the server

Commands:
    - create_group_requests.
        :param username (str)
        :return created(group_code) if successfully created, else creation_failed()
        task:
            Create a group

    - join_group_requests.
        :param group_code (str)
        :param username (str)
        :return joined() if group code exists, else group_not_found(group_code)
        task:
            Add sender to group

    - start_video_request
        sends all users within sender group a start_video_vote_started.
        wait for responses from everyone for a certain number of seconds.
        :return
            if someones denys: sends start_video_failed()
            if time passed: sends start_video_failed()
            if everyone sent start_video_vote_accept(): sends everyone start_succeeded()

    - start_video_vote_accept
        if senders group waits for starting:
            accepts the start request
        task:
            mark sender as accepted
            check if he is the last one

    - start_video_vote_deny
        if senders group waits for starting:
            deny the start request
        task:
            send everyone within the group start_video_failed()

    - pause_request
        :return
            if sender group has already started: sends everyone pause()
            else:  sends nothing

    - play_request
        :return
            if sender group has already started: sends everyone play()
            else:  sends nothing

    - stop_request
        :return
            if sender group has already started: sends everyone stop()
            else:  sends nothing

    - seek_request
        :param time (int in str format)
        :return
            if sender group has already started: sends everyone seek(time)
            else:  sends nothing

    - get_tick_rate
        :return tick_rate

    - send_message
        :param message
        :param receiver (name or empty space to everyone)
        :return
            if sender in group:  message_received

    - get_state
        :return
            if sender in group:  returns seek(time)
                if not group.playing: pause.

Responses:
    - created
        :param group_code (str)
        :param username (str)
        Confirmation That the group was created


    - creation_failed
        Group Creation Failed

    - joined
        :param group_code (str)
        :param username (str)
        Join Request Accepted

    - group_not_found
        :param group_code (str)
        The Given Group_Code does not exist

    - start_video_failed
        The start request had failed

    - start_video_succeeded
        The start request had succeeded, start movie

    - pause
        pause video

    - play
        unpause video

    - stop
        top video

    - seek
        :param time
        seek to the given time

    - tick_rate
        :param rate
        returns the tick rate of the server

    - message_received
        :param message
        :param sender
        :param receiver

    - users_list
        :param users (dict)
        returns the group users list + whether each user accepted or not

    - late start
        the user is late and the video has already started. tell him to load a video
        and then send get_state
Packet Protocol:
    command ? parameter1_name=parameter2_value & parameter2_name=parameter2_value ...  \n (no spaces)
    special characters must have backslash before
"""

import random
import time
import socket
import select
import warnings
import json

class AlwaysZero:
    def __add__(self, other):
        return 0

    def __radd__(self, other):
        return 0

    def __sub__(self, other):
        return 0

    def __rsub__(self, other):
        return 0

    def __mul__(self, other):
        return 0

    def __rmul__(self, other):
        return 0

    def __divmod__(self, other):
        return 0

    def __rdivmod__(self, other):
        return 0

    def __truediv__(self, other):
        return 0

    def __rtruediv__(self, other):
        return 0

    def __int__(self):
        return 0

    def __float__(self):
        return 0


class MovieTimer:
    def __init__(self):
        self.time = 0
        self.measure_time = AlwaysZero()
        self.freeze_measure_time = AlwaysZero()
        self.total_freeze_time = 0

    def start(self):
        self.measure_time = time.time()

    def freeze(self):
        self.freeze_measure_time = time.time()

    def unfreeze(self):
        self.total_freeze_time += 1000 * (time.time() - self.freeze_measure_time)
        self.freeze_measure_time = AlwaysZero()

    def reset(self):
        self.set_time(0)
        self.freeze()

    def set_time(self, time_):
        self.__init__()
        self.time = int(time_)
        self.start()

    def get_time(self):
        if isinstance(self.freeze_measure_time, AlwaysZero):
            return (self.time + int(1000 * (time.time() - self.measure_time))) - int(self.total_freeze_time)
        else:
            self.unfreeze()
            self.freeze()
            return (self.time + int(1000 * (time.time() - self.measure_time))) - int(self.total_freeze_time)

    def __int__(self):
        return self.get_time()


class Message:
    messages_to_send = []

    def __init__(self, socket_, message):
        self.socket = socket_
        self.message = message
        self.messages_to_send.append(self)

    def send(self):
        self.socket.send(self.message)
        self.messages_to_send.remove(self)

    @classmethod
    def remove_messages_to(cls, socket_):
        cls.messages_to_send = [msg for msg in cls.messages_to_send if not msg.socket == socket_]


class User:
    users_list = {}

    def __init__(self, socket_, address):
        self.socket = socket_
        self.address = address
        self.group = None
        self.users_list[self.socket] = self
        self.username = ''

    def set_group(self, group):
        self.group = group
        if not self.username:
            self.username = self.group.generate_name()
        self.group.add_user(self)

    def disconnect(self):
        if self.group is not None:
            self.group.remove_user(self)
        self.users_list.pop(self.socket)
        self.socket.close()

    def set_username(self, name):
        self.username = name

    def __eq__(self, other):
        if isinstance(other, User):
            return self.username == other.username
        return NotImplemented

    def __hash__(self):
        return self.username.__hash__()


class Group:
    group_list = {}  # code : group
    GROUP_CODE_LENGTH = 10
    TIME_IN_VOTE_MODE = 60  # in sec

    @classmethod
    def generate_code(cls):
        return '{{0:0{}d}}'.format(cls.GROUP_CODE_LENGTH).\
            format(random.randint(0, int('9' * cls.GROUP_CODE_LENGTH)))

    def __init__(self, user=None):
        self.code = self.generate_code()
        while self.code in self.group_list:
            self.code = self.generate_code()
        self.users = []
        self.in_vote_mode = SingleShotTimer(self.exit_vote_mode)
        self.accepted = {}  # later: user: accepted(bool)
        self.started = False
        self.name_numbers = iter(random.sample(range(1000), 1000))
        self.video_timer = MovieTimer()
        self.playing = False
        if user is not None:
            user.set_group(self)
        Group.group_list[self.code] = self

    def add_user(self, user):
        self.users.append(user)
        self.send_users_update()
        if self.started:
            Message(user.socket, Server.build_packet('late_start'))

    def remove_user(self, user):
        self.users.remove(user)
        if len(self.users) == 0:
            self.group_list.pop(self.code)

    def enter_vote_mode(self, user):
        """
        :param user: user who sent the request (he doesn't need to vote)
        sends all users start_video_vote_started
        """
        if not self.in_vote_mode:
            self.in_vote_mode.activate(self.TIME_IN_VOTE_MODE * 1000)
            self.accepted[user] = True
            for each_user in self.users:
                if each_user is not user:
                    Message(each_user.socket, Server.build_packet('start_video_vote_started'))
            if len(self.users) == 1:  # only one player in the group
                self.exit_vote_mode()
            self.send_users_update()

    def exit_vote_mode(self):
        if all([self.accepted.get(user, False) for user in self.users]):
            self.started = True
            self.playing = True

            packet = Server.build_packet('start_video_succeeded')
            for user in self.users:
                Message(user.socket, packet)
            self.video_timer.start()
        else:
            packet = Server.build_packet('start_video_failed')
            for user in self.users:
                Message(user.socket, packet)

        self.accepted.clear()
        self.send_users_update()
        self.in_vote_mode.reset()

    def accept_video_vote(self, user):
        if self.in_vote_mode:
            self.accepted[user] = True
        if len(self.accepted) == len(self.users):
            self.exit_vote_mode()
        self.send_users_update()

    def deny_video_vote(self, user):
        if self.in_vote_mode:
            self.exit_vote_mode()
        self.send_users_update()

    def pause(self):
        if self.started:
            self.playing = False
            self.video_timer.freeze()
            packet = Server.build_packet('pause')
            for user in self.users:
                Message(user.socket, packet)

    def play(self):
        if self.started:
            self.playing = True
            self.video_timer.unfreeze()
            packet = Server.build_packet('play')
            for user in self.users:
                Message(user.socket, packet)

    def stop(self):
        if self.started:
            self.video_timer.reset()
            packet = Server.build_packet('stop')
            for user in self.users:
                Message(user.socket, packet)

    def seek(self, ms):
        if self.started:
            self.video_timer.set_time(ms)
            packet = Server.build_packet('seek', time=ms)
            for user in self.users:
                Message(user.socket, packet)

    def send_messages_to(self, packet, destination, except_=()):
        if destination == ' ':
            for user in self.users:
                if user.username not in except_:
                    Message(user.socket, packet)
        else:  # destination is a specific name
            for user in self.users:
                if user.username == destination:
                    Message(user.socket, packet)
                    break

    def generate_name(self):
        return 'User-{0:03d}'.format(next(self.name_numbers))

    def send_users_update(self):
        names = {user.username: self.accepted.get(user, False) for user in self.users}
        self.send_messages_to(Server.build_packet('users_list', users=json.dumps(names)), ' ')

    def legal_name(self, name) -> bool:
        return (name != "Everyone") and (name not in [user.username for user in self.users])


class SingleShotTimer:
    inf = float('inf')
    timers_list = []

    def __init__(self, function):
        self.timer = self.inf
        self.activated = False
        self.function = function
        self.timers_list.append(self)

    def activate(self, ms):
        self.timer = ms
        self.activated = True

    def reset(self):
        self.timer = self.inf
        self.activated = False

    def update(self, elapsed):
        if self.activated:
            self.timer -= elapsed
            if self.timer <= 0:
                self.function()
                self.timer = 0
                self.timers_list.remove(self)

    def active(self):
        return self.activated

    def __bool__(self):
        return self.active()

    @classmethod
    def update_all(cls, elapsed):
        for timer in cls.timers_list:
            timer.update(elapsed)


class Server:
    TICKS_PER_SECOND = 25
    PORT = 35241
    IP = "0.0.0.0"

    open_client_sockets = []

    def __init__(self):
        self.commands = {
            "create_group_requests": self.create_group_requests,
            "start_video_request": self.start_video_request,
            "join_group_request": self.join_group_request,
            "start_video_vote_accept": self.start_video_vote_accept,
            "start_video_vote_deny": self.start_video_vote_deny,
            "pause_request": self.pause_request,
            "play_request": self.play_request,
            "stop_request": self.stop_request,
            "seek_request": self.seek_request,
            "get_tick_rate": self.get_tick_rate,
            "disconnect": self.disconnect,
            "send_message": self.send_message,
            "get_state": self.get_group_state
        }
        self.server_socket = socket.socket()
        self.server_socket.setblocking(False)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen(1000)
        self.loop()

    def loop(self):
        n = 0
        while True:
            start_time = time.time()
            self.tick()
            time.sleep(1/self.TICKS_PER_SECOND)
            SingleShotTimer.update_all((time.time() - start_time) * 1000)
            if n == 25:
                # print([] if not Group.group_list else [u.username for u in list(Group.group_list.values())[0].users])
                print([] if not Group.group_list else list(Group.group_list.values())[0].video_timer.get_time())
                n = 0
            n += 1

    def tick(self):
        read_list, write_list, _ = select.select([self.server_socket] + self.open_client_sockets,
                                                 self.open_client_sockets, [])
        for notified_socket in read_list:
            if notified_socket is self.server_socket:
                self.receive_connection()
            else:
                connected = self.handle_request(notified_socket)
                if not connected:
                    self.disconnect_user(User.users_list[notified_socket])

        self.send_waiting_messages(write_list)

    def receive_connection(self):
        client_socket, client_address = self.server_socket.accept()
        self.open_client_sockets.append(client_socket)
        User(client_socket, client_address)

    def handle_request(self, client_socket):
        try:
            data = bytearray()
            while True:
                try:
                    new = client_socket.recv(4069)
                    if new:
                        data.extend(new)
                    else:
                        break
                except BlockingIOError:
                    break

            if not data:
                print("empty message...")
                return False

            requests = self.smart_split(data.decode(), '\n')
            for request in requests:
                command, kwargs = self.split_message(request)
                self.commands[command](User.users_list[client_socket], kwargs)
        except Exception as e:
            warnings.warn("Something broken\n " + repr(e))
            return False
        return True

    def disconnect_user(self, user: User):
        self.open_client_sockets.remove(user.socket)
        Message.remove_messages_to(user.socket)
        user.disconnect()

    # commands:
    def create_group_requests(self, user: User, kwargs):
        name = kwargs['name']
        if name:  # else stay with default name
            user.set_username(name)
        group = Group(user)
        Message(user.socket, self.build_packet('created', group_code=group.code, username=user.username))

    def join_group_request(self, user: User, kwargs):
        code = None
        try:
            name = kwargs['name']
            code = kwargs['group_code']
            group = Group.group_list[code]
            if name and group.legal_name(name):  # else stay with default name
                user.set_username(name)

            user.set_group(group)
            Message(user.socket, self.build_packet("joined", group_code=code, username=user.username))
        except KeyError:
            Message(user.socket, self.build_packet("group_not_found", group_code=code))

    def start_video_request(self, user: User, kwargs):
        group = user.group
        if group is not None:
            group.enter_vote_mode(user)

    def start_video_vote_accept(self, user: User, kwargs):
        group = user.group
        if group is not None:
            group.accept_video_vote(user)

    def start_video_vote_deny(self, user: User, kwargs):
        group = user.group
        if group is not None:
            group.deny_video_vote(user)

    def pause_request(self, user: User, kwargs):
        group = user.group
        if group is not None:
            group.pause()

    def play_request(self, user: User, kwargs):
        group = user.group
        if group is not None:
            group.play()

    def stop_request(self, user: User, kwargs):
        group = user.group
        if group is not None:
            group.stop()

    def seek_request(self, user: User, kwargs):
        ms = kwargs['time']
        print("got request to: ", ms)
        group = user.group
        if group is not None:
            group.seek(ms)

    def get_tick_rate(self, user: User, kwargs):
        Message(user.socket, self.build_packet('tick_rate', rate=self.TICKS_PER_SECOND))

    def disconnect(self, user: User, kwargs):
        self.disconnect_user(user)

    def send_message(self, user, kwargs):
        message = kwargs['message']
        destination = kwargs['receiver']
        user.group.send_messages_to(self.build_packet('message_received', message=message, receiver=destination,
                                                      sender=user.username), except_=(user.username,),
                                    destination=' ' if destination == 'Everyone' else destination)

    def get_group_state(self, user, kwargs):
        group = user.group
        if group is not None:
            Message(user.socket, self.build_packet('seek', time=int(group.video_timer)))
            if not group.playing:
                Message(user.socket, self.build_packet('pause'))

    # /commands

    @staticmethod
    def send_waiting_messages(write_list):
        for message in Message.messages_to_send:
            if message.socket in write_list:
                message.send()

    @staticmethod
    def format_string(string):
        r"""Replaces %, & and = with \%, \& and \= respectively"""
        return str(string).replace('%', r'\%').replace('&', r'\&').replace('=', r'\=')

    @classmethod
    def build_packet(cls, command: str, **parameters):
        return cls.format_string(command).encode() + (b'?' if parameters else b'') + ('&'.join(
            ['{}={}'.format(cls.format_string(param), cls.format_string(val))
             for param, val in parameters.items()])).encode() + b'\n'

    @classmethod
    def split_message(cls, request: str):
        command, *arguments = cls.smart_split(request, '?')
        if arguments:
            args = [cls.smart_split(i, '=') for i in cls.smart_split(arguments[0], '&')]
            for arg in args:
                if len(arg) == 1:  # only argument but not value, assign default value.
                    arg.append('')
            kwargs = dict(args)
        else:
            kwargs = {}
        return command, kwargs

    @staticmethod
    def smart_split(string, separator, saver='\\'):
        """Split string by the separator, as long as saver is not present before the separator.
        for example: string='Hello0Dear0W\0rld, separator='0', saver='\' returns ['Hello', 'Dear', 'W0rld']"""
        splited = string.split(separator)
        new_list = []
        i = 0
        while i < len(splited):
            item = splited[i]
            if item:
                if item[-1] == saver and not i+1 == len(splited):  # merge it with the next item
                    item = item[:-1]
                    item += separator + splited[i+1]
                    i += 1
                new_list.append(item)
            i += 1

        return new_list

    @staticmethod
    def encode_list(args):
        return ','.join(arg.replace(',', r'\,') for arg in args)

    @classmethod
    def decode_list(cls, lst):
        return cls.smart_split(lst, ',')


if __name__ == '__main__':
    Server()
