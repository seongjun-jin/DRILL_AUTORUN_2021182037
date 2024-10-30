from pico2d import *
from State_Machine import *

#idle 상태에서 수행할 4개의 함수를 하나에 그루핑
class Idle:
    @staticmethod
    def enter(boy, e):
        if e[0] == 'TIME_OUT':
            # 타임아웃에서 전이되면 현재 방향(action)과 face_dir을 그대로 유지
            if boy.action == 1:
                boy.action = 3
                boy.frame = 0
            elif boy.action == 0:
                boy.action = 2
                boy.frame = 0


        if left_up(e) or right_down(e) :
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e) :
            boy.action = 3
            boy.face_dir = 1

        boy.dir = 0
        boy.frame = 0

        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 1:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1: #오른쪽 방향
            boy.image.clip_composite_draw(
                boy.frame * 100,300,100,100, 3.141592 / 2,
                '',boy.x - 25, boy.y - 25, 100, 100
            )
        elif boy.face_dir == -1: #왼쪽 방향
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100, -3.141592 / 2,
                '', boy.x + 25, boy.y - 25, 100, 100
            )
        pass

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.action = 1
            boy.dir = 1
            boy.face_dir = 1
        elif left_down(e) or right_up(e):
            boy.action = 0
            boy.dir = -1
            boy.face_dir = -1

        boy.frame = 0

        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 1
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame*100, boy.action*100 ,100,100,
            boy.x, boy.y
        )
        pass

class Auto_Run:
    @staticmethod
    def enter(boy, e):
        if boy.face_dir == 1:
            boy.action = 1
            boy.dir = 1
        elif boy.face_dir == -1:
            boy.action = 0
            boy.dir = -1

        boy.autorun_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):
        boy.dir = 0
        pass

    @staticmethod
    def do(boy):
        if (boy.x <= 0):
            boy.face_dir = 1
            boy.action = 1
            boy.dir = 1

        elif (boy.x >= 800):
            boy.face_dir = -1
            boy.action = 0
            boy.dir = -1

        if get_time() - boy.autorun_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))

        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 20
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_draw(
                boy.frame * 100, 100, 100, 100,
                boy.x, boy.y + 25, 200, 200
            )
        elif boy.face_dir == -1:
            boy.image.clip_draw(
                boy.frame * 100, 0, 100, 100,
                boy.x, boy.y + 25, 200, 200
            )

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 어떤 객체를 위한 상태머신인가
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, auto_on: Auto_Run},
                #Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                Auto_Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Idle}
            }
        )
        #객체생성 x 직접 idle이라는 상태를 정의

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        #인풋이벤트 -> 스테이트머신용 이벤트:(이벤트종류, 값)
        self.state_machine.add_event(
             ['INPUT', event]
        )
        pass

    def draw(self):
        self.state_machine.draw()

