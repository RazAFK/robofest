from enum import StrEnum

class Motor(StrEnum):
    fr = 'front_right'
    fl = 'front_left'
    br = 'back_right'
    bl = 'back_left'

    class Pins(StrEnum):
        m_plus = 'm_plus'
        m_minus = 'm_minus'
        arduino_v = 'arduino_v'
        ground = 'ground'
        pin_a = 'pin_a'
        pin_b = 'pin_b'

class Driver(StrEnum):
    flash = 'flash'
    a4988 = 'a4988'

    class Adress_flash(StrEnum):
        A = '_A'
        B = '_B'
        C = '_C'
        D = '_D'
        E = '_E'

    class Pins_flash(StrEnum):
        plus_12v = 'plus_12v'
        minus_12v = 'minus_12v'
        arduino_v_out = 'arduino_v_out'
        ground_out = 'ground_out'
        pin_a = 'pin_a'
        pin_b = 'pin_b'

        arduino_v_in = 'arduino_v_in'
        ground_in = 'ground_in'
        scl = 'scl'
        sda = 'sda'
    class Pins_a4988(StrEnum):
        plus_5v = 'plus_5v'
        minus_5v = 'minus_5v'
        arduino_v = 'arduino_v'
        ground = 'ground'
        dir = 'dir'
        step = 'step'
        en = 'en'

class Conventor(StrEnum):
    conventor_12v = 'conventor_12v'
    conventor_5v = 'conventor_5v'

    class Pins(StrEnum):
        in_plus = 'v_plus'
        in_minus = 'in_minus'
        out_plus = 'out_plus'
        out_minus = 'out_minus'

class Power(StrEnum):

    name = 'power_unit'

    class Pins(StrEnum):
        plus = 'plus'
        minus = 'minus'

class Arduino(StrEnum):

    name = 'arduino_nano'

    class Pins:
        arduino_v = 'arduino_v'
        ground = 'ground'
        A = {
            0: 'A0',
            1: 'A1',
            2: 'A2',
            3: 'A3',
            4: 'A4',
            5: 'A5',
            6: 'A6'
        }
        D = {    
            2: 'D2',
            3: 'D3',
            4: 'D4',
            5: 'D5',
            6: 'D6',
            7: 'D7',
            8: 'D8',
            9: 'D9',
            10: 'D10',
            11: 'D11',
            12: 'D12',
        }
        sda = A[4]
        scl = A[5]

class Bus(StrEnum):
    
    i2c_bus = 'i2c_bus'
    power_bus = 'power_bus'

    class Pins_i2c:
        arduino_v = {
            'in': 'arduino_v_in',
            1: 'v_out_1',
            2: 'v_out_2',
            3: 'v_out_3',
            4: 'v_out_4',
            5: 'v_out_5',
        }
        ground = {
            'in': 'ground_in',
            1: 'g_out_1',
            2: 'g_out_2',
            3: 'g_out_3',
            4: 'g_out_4',
            5: 'g_out_5',
        }
        scl = {
            'in': 'scl_in',
            1: 'scl_out_1',
            2: 'scl_out_2',
            3: 'scl_out_3',
            4: 'scl_out_4',
            5: 'scl_out_5',
        }
        sda = {
            'in': 'sda_in',
            1: 'sda_out_1',
            2: 'sda_out_2',
            3: 'sda_out_3',
            4: 'sda_out_4',
            5: 'sda_out_5',
        }

    class Pins_power:
        p_in = {
            '+': '+'
        }
        m_in = {
            '-': '-'
        }
        p_out = {
            1: '+',
            2: '+',
            3: '+',
            4: '+',
            5: '+',
            6: '+',
        }
        m_out = {
            1: '-',
            2: '-',
            3: '-',
            4: '-',
            5: '-',
            6: '-',
        }


class Element:
    def __init__(self, name: str, connectors: dict):
        self.name = name
        self.con = connectors

power = Element(Power.name, {
    Power.Pins.plus: 'None',
    Power.Pins.minus: 'None'
})

fr = Element(Motor.fr, {
    Motor.Pins.arduino_v: 'None',
    Motor.Pins.ground: 'None',
    Motor.Pins.m_minus: 'None',
    Motor.Pins.m_plus: 'None',
    Motor.Pins.pin_a: 'None',
    Motor.Pins.pin_b: 'None'   
})
fl = Element(Motor.fl, {
    Motor.Pins.arduino_v: 'None',
    Motor.Pins.ground: 'None',
    Motor.Pins.m_minus: 'None',
    Motor.Pins.m_plus: 'None',
    Motor.Pins.pin_a: 'None',
    Motor.Pins.pin_b: 'None'   
})
br = Element(Motor.br, {
    Motor.Pins.arduino_v: 'None',
    Motor.Pins.ground: 'None',
    Motor.Pins.m_minus: 'None',
    Motor.Pins.m_plus: 'None',
    Motor.Pins.pin_a: 'None',
    Motor.Pins.pin_b: 'None'   
})
bl = Element(Motor.bl, {
    Motor.Pins.arduino_v: 'None',
    Motor.Pins.ground: 'None',
    Motor.Pins.m_minus: 'None',
    Motor.Pins.m_plus: 'None',
    Motor.Pins.pin_a: 'None',
    Motor.Pins.pin_b: 'None'   
})


mot_dr_f_a = fr
dr_f_a = Element(Driver.flash+Driver.Adress_flash.A, {
    Driver.flash.Pins_flash.arduino_v_in: 'None',
    Driver.flash.Pins_flash.ground_in: 'None',
    Driver.flash.Pins_flash.scl: 'None',
    Driver.flash.Pins_flash.sda: 'None',

    Driver.flash.Pins_flash.arduino_v_out: mot_dr_f_a.name + '_'  + Motor.Pins.arduino_v,
    Driver.flash.Pins_flash.ground_out: mot_dr_f_a.name + '_'  + Motor.Pins.ground,
    Driver.flash.Pins_flash.plus_12v: mot_dr_f_a.name + '_'  + Motor.Pins.m_plus,
    Driver.flash.Pins_flash.minus_12v: mot_dr_f_a.name + '_'  + Motor.Pins.m_minus,
    Driver.flash.Pins_flash.pin_a: mot_dr_f_a.name + '_'  + Motor.Pins.pin_a,
    Driver.flash.Pins_flash.pin_b: mot_dr_f_a.name + '_'  + Motor.Pins.pin_b,   
})

mot_dr_f_b = fl
dr_f_b = Element(Driver.flash+Driver.Adress_flash.B, {
    Driver.flash.Pins_flash.arduino_v_in: 'None',
    Driver.flash.Pins_flash.ground_in: 'None',
    Driver.flash.Pins_flash.scl: 'None',
    Driver.flash.Pins_flash.sda: 'None',

    Driver.flash.Pins_flash.arduino_v_out: mot_dr_f_b.name + '_'  + Motor.Pins.arduino_v,
    Driver.flash.Pins_flash.ground_out: mot_dr_f_b.name + '_'  + Motor.Pins.ground,
    Driver.flash.Pins_flash.plus_12v: mot_dr_f_b.name + '_'  + Motor.Pins.m_plus,
    Driver.flash.Pins_flash.minus_12v: mot_dr_f_b.name + '_'  + Motor.Pins.m_minus,
    Driver.flash.Pins_flash.pin_a: mot_dr_f_b.name + '_'  + Motor.Pins.pin_a,
    Driver.flash.Pins_flash.pin_b: mot_dr_f_b.name + '_'  + Motor.Pins.pin_b,   
})

mot_dr_f_c = br
dr_f_c = Element(Driver.flash+Driver.Adress_flash.C, {
    Driver.flash.Pins_flash.arduino_v_in: 'None',
    Driver.flash.Pins_flash.ground_in: 'None',
    Driver.flash.Pins_flash.scl: 'None',
    Driver.flash.Pins_flash.sda: 'None',

    Driver.flash.Pins_flash.arduino_v_out: mot_dr_f_c.name + '_'  + Motor.Pins.arduino_v,
    Driver.flash.Pins_flash.ground_out: mot_dr_f_c.name + '_'  + Motor.Pins.ground,
    Driver.flash.Pins_flash.plus_12v: mot_dr_f_c.name + '_'  + Motor.Pins.m_plus,
    Driver.flash.Pins_flash.minus_12v: mot_dr_f_c.name + '_'  + Motor.Pins.m_minus,
    Driver.flash.Pins_flash.pin_a: mot_dr_f_c.name + '_'  + Motor.Pins.pin_a,
    Driver.flash.Pins_flash.pin_b: mot_dr_f_c.name + '_'  + Motor.Pins.pin_b,   
})

mot_dr_f_d = bl
dr_f_d = Element(Driver.flash+Driver.Adress_flash.D, {
    Driver.flash.Pins_flash.arduino_v_in: 'None',
    Driver.flash.Pins_flash.ground_in: 'None',
    Driver.flash.Pins_flash.scl: 'None',
    Driver.flash.Pins_flash.sda: 'None',
        

    Driver.flash.Pins_flash.arduino_v_out: mot_dr_f_d.name + '_'  + Motor.Pins.arduino_v,
    Driver.flash.Pins_flash.ground_out: mot_dr_f_d.name + '_'  + Motor.Pins.ground,
    Driver.flash.Pins_flash.plus_12v: mot_dr_f_d.name + '_'  + Motor.Pins.m_plus,
    Driver.flash.Pins_flash.minus_12v: mot_dr_f_d.name + '_'  + Motor.Pins.m_minus,
    Driver.flash.Pins_flash.pin_a: mot_dr_f_d.name + '_'  + Motor.Pins.pin_a,
    Driver.flash.Pins_flash.pin_b: mot_dr_f_d.name + '_'  + Motor.Pins.pin_b,   
})

i2c_bus = Element(Bus.i2c_bus, {
    Bus.Pins_i2c.arduino_v['in']: 'None',
    Bus.Pins_i2c.ground['in']: 'None',
    Bus.Pins_i2c.scl['in']: 'None',
    Bus.Pins_i2c.sda['in']: 'None',

    Bus.Pins_i2c.arduino_v[1]: dr_f_a.name + '_'  + dr_f_a.con[Driver.flash.Pins_flash.arduino_v_in],
    Bus.Pins_i2c.ground[1]: dr_f_a.name + '_'  + dr_f_a.con[Driver.flash.Pins_flash.ground_in],
    Bus.Pins_i2c.scl[1]: dr_f_a.name + '_'  + dr_f_a.con[Driver.flash.Pins_flash.scl],
    Bus.Pins_i2c.sda[1]: dr_f_a.name + '_'  + dr_f_a.con[Driver.flash.Pins_flash.sda],

    Bus.Pins_i2c.arduino_v[2]: dr_f_b.name + '_'  + dr_f_b.con[Driver.flash.Pins_flash.arduino_v_in],
    Bus.Pins_i2c.ground[2]: dr_f_b.name + '_'  + dr_f_b.con[Driver.flash.Pins_flash.ground_in],
    Bus.Pins_i2c.scl[2]: dr_f_b.name + '_'  + dr_f_b.con[Driver.flash.Pins_flash.scl],
    Bus.Pins_i2c.sda[2]: dr_f_b.name + '_'  + dr_f_b.con[Driver.flash.Pins_flash.sda],

    Bus.Pins_i2c.arduino_v[3]: dr_f_c.name + '_'  + dr_f_c.con[Driver.flash.Pins_flash.arduino_v_in],
    Bus.Pins_i2c.ground[3]: dr_f_c.name + '_'  + dr_f_c.con[Driver.flash.Pins_flash.ground_in],
    Bus.Pins_i2c.scl[3]: dr_f_c.name + '_'  + dr_f_c.con[Driver.flash.Pins_flash.scl],
    Bus.Pins_i2c.sda[3]: dr_f_c.name + '_'  + dr_f_c.con[Driver.flash.Pins_flash.sda],

    Bus.Pins_i2c.arduino_v[4]: dr_f_d.name + '_'  + dr_f_d.con[Driver.flash.Pins_flash.arduino_v_in],
    Bus.Pins_i2c.ground[4]: dr_f_d.name + '_'  + dr_f_d.con[Driver.flash.Pins_flash.ground_in],
    Bus.Pins_i2c.scl[4]: dr_f_d.name + '_'  + dr_f_d.con[Driver.flash.Pins_flash.scl],
    Bus.Pins_i2c.sda[4]: dr_f_d.name + '_'  + dr_f_d.con[Driver.flash.Pins_flash.sda],
})

arduino = Element(Arduino.name, {
    Arduino.Pins.arduino_v: i2c_bus.name + '_'  + i2c_bus.con[Bus.Pins_i2c.arduino_v['in']],
    Arduino.Pins.ground: i2c_bus.name + '_'  + i2c_bus.con[Bus.Pins_i2c.ground['in']],
    Arduino.Pins.scl: i2c_bus.name + '_'  + i2c_bus.con[Bus.Pins_i2c.scl['in']],
    Arduino.Pins.sda: i2c_bus.name + '_'  + i2c_bus.con[Bus.Pins_i2c.sda['in']],
})

elements = [power, fr, fl, br, bl, dr_f_a, dr_f_b, dr_f_c, dr_f_d, i2c_bus, arduino]

def subgraph(elem: Element):
    ret = f'subgraph {elem.name} [{elem.name}]\n'
    for key, value in elem.con.items():
        pin = f'\t\t{elem.name + '_' + key}(( {key} ))'
        if value != 'None':
            pin += f' --- {value}(( {value} ))'
        ret += f'{pin}\n'
    ret += '\tend\n'
    return ret

def link(elem: Element):
    ret = ''
    for key, value in elem.con.items():
        if value == 'None': continue
        pin = f'{elem.name + '_' + key} --- {value}'
        ret += f'{pin}\n'
    return ret


with open('src/documentation/scheme.mmd', 'w') as file:
    file.write(
'''%%{init: {'flowchart': {'curve': 'stepChild'}}}%%
graph LR
    classDef redPin fill:#f00, stroke:#f00, width:8px, height:8px, color:#000, font-weight:bold;
    classDef bluePin fill:#00f, stroke:#00f, width:8px, height:8px, color:#000, font-weight:bold;
    
    classDef box fill:#fff,stroke:#000,stroke-width:2px;
''' + 
f'''
{'\n'.join([subgraph(element) for element in elements])}
{link(power)}

{link(fr)}

{link(fl)}

{link(br)}

{link(bl)}

{link(arduino)}
    
    linkStyle 2 stroke:#f00,stroke-width:2px;
    linkStyle 3 stroke:#00f,stroke-width:2px;
    
    linkStyle 0 stroke:#f00,stroke-width:2px;
    linkStyle 1 stroke:#00f,stroke-width:2px;
''')
