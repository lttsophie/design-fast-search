# -*- coding: utf-8 -*-


import itertools
import os
import random

from psychopy import core, visual, gui, data, event

# the first window after running the experiment with empty fields for name
# and age of the participant
dlg = gui.Dlg(title=u"Информация")
dlg.addText(u'Об испытуемом:')
dlg.addField(u'Фамилия:')
dlg.addField(u'Возраст:')

ok_data = dlg.show()  # show dialog and wait for OK or Cancel
if not dlg.OK:
    print('user cancelled')
    exit()

# creating window for all experiment
window = visual.Window([1920, 1080], monitor="test_monitor", units="pix",
                       color=(250, 250, 250))

# picture's directory
pics_dir = 'stimuli'

# instruction to the experiment
message = visual.TextStim(window, color=(0, 0, 0),
                          text=u'В данном эксперименте вам предстоит '
                               u'запоминать объект, предъявляемый в начале'
                               u'каждого предъявления на ограниченное количество'
                               u'времени, а затем искать его среди других'
                               u'объектов на экране. Если вы обнаружили запомненный'
                               u'объект на экране поиска нажмите кнопку "СТРЕЛКА ВПРАВО",'
                               u'если вы не обнаружили запомненный вами объект на экране,'
                               u'нажмите кнопку "СТРЕЛКА ВЛЕВО". Во время эксперимента'
                               u'старайтесь действовать как можно быстрее и точнее.'
                               u'Если у вас остались вопросы, задайте их экспериментатору.'
                               u'Для перехода к тренировочной серии нажмите "ПРОБЕЛ"'

                          )
message.draw()
window.flip()

event.waitKeys(keyList=["space"])

event.clearEvents()

clock = core.Clock()


def create_trails_one_cond():
    with_ts = []
    wo_ts = []
    for ts in range(1, 31):
        with_target = list(range(1, 31))
        set_3 = []
        set_6 = []
        set_9 = []
        set_3.append(ts)
        set_3.append(ts)
        set_6.append(ts)
        set_6.append(ts)
        set_9.append(ts)
        set_9.append(ts)
        with_target.remove(ts)
        set_3 += set(random.sample(with_target, 2))
        set_6 += set(random.sample(with_target, 5))
        set_9 += set(random.sample(with_target, 8))
        with_ts.append(set_3)
        with_ts.append(set_6)
        with_ts.append(set_9)
    for wots in range(0, 10):
        wo_target = list(range(1, 31))
        set_wo_3 = list(set(random.sample(wo_target, 4)))
        set_wo_6 = list(set(random.sample(wo_target, 7)))
        set_wo_9 = list(set(random.sample(wo_target, 10)))
        wo_ts.append(set_wo_3)
        wo_ts.append(set_wo_6)
        wo_ts.append(set_wo_9)
    return with_ts, wo_ts


def create_trail_list():
    with_ts_flat, wo_ts_flat = create_trails_one_cond()
    with_ts_shad, wo_ts_shad = create_trails_one_cond()
    with_ts_grad, wo_ts_grad = create_trails_one_cond()
    with_ts_sg, wo_ts_sg = create_trails_one_cond()
    condition_flat = with_ts_flat + wo_ts_flat
    condition_shad = with_ts_shad + wo_ts_shad
    condition_grad = with_ts_grad + wo_ts_grad
    condition_sg = with_ts_sg + wo_ts_sg
    all_trails = []
    for i in range(0, len(condition_flat)):
        flat = list(map(lambda x: str(x) + 'f.png', condition_flat[i]))
        shadow = list(map(lambda x: str(x) + 'fs.png', condition_shad[i]))
        gradient = list(map(lambda x: str(x) + 'g.png', condition_grad[i]))
        grad_shad = list(map(lambda x: str(x) + 'gs.png', condition_sg[i]))
        all_trails.append(flat)
        all_trails.append(shadow)
        all_trails.append(gradient)
        all_trails.append(grad_shad)
    random.shuffle(all_trails)
    return all_trails


all_trails = create_trail_list()


def show_stimuli(name, pos):
    stim = visual.ImageStim(window, pos=pos)
    stim.setImage(os.path.join(pics_dir, name))
    stim.size = [150, 150]
    stim.draw()


# this function creates positions of objects for all objects in trail
def get_possible_trail_positions():
    def create_pos(x, y, cell=250, margin=50):
        return (int(x * cell * 1.8 + margin + random.randint(-20, 20)) - 675,
                int(y * cell + margin + random.randint(-20, 20)) - 375)

    positions = set()
    for x in range(0, 4):
        for y in range(0, 4):
            positions.add(create_pos(x, y))
    return positions


for t in range(0, len(all_trails)):
    show_stimuli(all_trails[t][0], pos=[0, 0])
    window.flip()
    core.wait(1)
    window.flip()
    dest = all_trails[t][1:]
    pos = get_possible_trail_positions()

    stimuli = zip(dest, pos)
    for (n, pos) in stimuli:
        show_stimuli(n, pos)
    window.flip()
    clock.reset()
    key = event.waitKeys(keyList=["left", "right", "escape"])
    if key[0] == "escape":
        experiment_in_progress = False
        break
    window.flip()

    event.clearEvents()
message = visual.TextStim(window, text=u'Спасибо, что были с нами!')
message.draw()
window.flip()
core.wait(5)
window.flip()
