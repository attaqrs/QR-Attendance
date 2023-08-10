import qrcode
import requests
import socket as s
import pyray as pr

def start_session(server_url):
    hashes = requests.get(server_url + '/start_session?section=' + section).text.split()
    print('hashes:', hashes)
    return hashes[0], hashes[1]

def end_session(server_url, private_hash):
    print(requests.get(server_url + '/end_session?private_hash=' + private_hash).text)

def get_cur_attendance(server_url):
    global atts
    atts_response = requests.get(server_url + '/get_cur_attendance').text
    if atts_response:
        atts = atts_response.split(';')

section = ''
server_url = 'http://' + s.gethostbyname(s.gethostname()) + ':8080'
hash, private_hash = '', ''

def gen_qr():
    global qr_tex
    qr_text = server_url + '/mark_attendance?hash=' + hash
    qr = qrcode.make(qr_text)
    qr.save('qr.png')
    qr_tex = pr.load_texture('qr.png')

width, height = 1366, 768
fps = 60
pr.init_window(width, height, 'QR Attendance')
pr.set_target_fps(fps)

f = pr.get_font_default()

qr_size = 500

frames = 0

atts = []
atts_scroll = 100

cur_screen = 'menu'

## menu variables
x = 1366 // 2 - 150
y = 768 // 2 + 768 // 15
w = 300
h = 100

## attendance variables
qr_t = None
x2 = 1366 // 2 - 100
y2 = 768 // 2 + 768 // 15 + 120
w2 = 200
h2 = 70

sections = 'ABCDEFGHIJKLMNO'

while not pr.window_should_close():
    atts_scroll += pr.get_mouse_wheel_move() * 40

    pr.begin_drawing()
    pr.clear_background(pr.WHITE)

    # pr.draw_texture_ex(qr_tex, pr.Vector2((width - qr_size) // 10, (height - qr_size) // 2), 0, qr_size / qr_tex.width, pr.WHITE)
    # pr.gui_group_box(pr.Rectangle((width - qr_size) // 10, (height - qr_size) // 2, qr_size, qr_size), 'Scan this QR code')

    # for indx, att in enumerate(atts):
    #     pr.draw_text(att, 750, int(atts_scroll + 50 * indx), 19, pr.BLACK)
    # pr.draw_text('Attendances marked so far:', 750, 50, 36, pr.BLACK)

    if cur_screen == 'menu':
        # main menu
        genQR_rec = pr.Rectangle(x, y, w, h)
        genQR_b = pr.gui_button(genQR_rec, "Generate QR")

        #section buttons
        buttons_x, buttons_y = 1366 // 2 - 175 , 200
        for i in range(5):
            for j in range(3):
                if pr.gui_button(pr.Rectangle(buttons_x + 70 * i, buttons_y + 50 * j, 70, 50), sections[j * 5 + i]):
                    section = sections[j * 5 + i]
                    print(section)
        pr.draw_text("AttaQR", buttons_x + 100, 80, 40, pr.BLACK)
        pr.draw_text("Select Section", buttons_x + 65 ,buttons_y - 40,30, pr.BLACK)

        if genQR_b:
            if section:
                cur_screen = 'attendance'
                hash, private_hash = start_session(server_url)
                gen_qr()
    
    elif cur_screen == 'attendance':
        # attendance
        pr.draw_texture_ex(qr_tex, pr.Vector2((width - qr_size) // 10, (height - qr_size) // 2 - 100), 0, qr_size / qr_tex.width, pr.WHITE)
        # pr.draw_texture_ex(qr_t, pr.Vector2(505, 70), 0.0, 0.8, pr.WHITE)
        get_rep = pr.Rectangle(((width - qr_size) // 10) // 2 + 150, (height - qr_size) + 275 , w ,h)
        get_rep_b = pr.gui_button( get_rep, "End Session")
        if get_rep_b:
            end_session(server_url, private_hash)
            break

        
        for indx, att in enumerate(atts):
            pr.draw_text(att, 700, int(atts_scroll + 50 * indx), f.baseSize * 2, pr.BLACK)
        pr.draw_text('Attendances marked so far: ' + str(len(atts)-(1 if len(atts) else 0)), 700, 50, f.baseSize * 4, pr.BLACK)

    pr.draw_fps(10, 10)
    pr.end_drawing()

    frames += 1
    if frames >= fps * 2:
        frames = 0
        get_cur_attendance(server_url)
        print(atts)

end_session(server_url, private_hash)
pr.close_window()
