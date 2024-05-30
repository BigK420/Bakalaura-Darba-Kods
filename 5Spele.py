# -*- coding: utf-8 -*-
import tkinter as tk
from PIL import Image, ImageTk 

class NumberGameApp:
    def __init__(self, master):
        # Galvenā ekrāna palaišanai
        self.master = master
        master.title("5 Soļu Ciparu Spēle.")
        master.resizable(False, False)

        # Palaiž sākuma ekrānu
        self.start_frame = tk.Frame(master)
        self.start_frame.pack(fill='both', expand=True)

        title = tk.Label(self.start_frame, text="5 Soļu Ciparu Spēle", font=('Helvetica', 24, 'bold'))
        title.pack(pady=20)

        instructions = tk.Label(self.start_frame, text="Spēlētēja uzdevums ir uzpiest uz\n"
                                                      "skaitļiem no 1 līdz 49 pareizā secībā.\n"
                                                      "Ir dotas 30 sekundes, lai to izdarītu.\n"
                                                      "Rezultāts tiks fiksēts.",
                                font=('Helvetica', 14), justify=tk.LEFT)
        instructions.pack(pady=10)

        start_button = tk.Button(self.start_frame, text="Sākt spēli", command=lambda: self.setup_game(1), font=('Helvetica', 18))
        start_button.pack(pady=20)

        self.last_correct_number_pressed = None
        self.best_number_part = [None, None, None, None, None, None]  # Labākie skaitļi katrai daļai
        self.current_game_part = 1  # Pašreizējā spēles daļa
        self.periods_needed = [0, 0]  # Cikli, kas nepieciešami 5. un 6. daļai
        self.correct_numbers = [18, 42] # Glabā sevī datus par pareizajiem skatļiem 5 un 6 daļai
        self.found_numbers = set()  # Atrastie skaitļi 5. un 6. daļai
        self.timer = None  # Taimeris

    def setup_game(self, game_part):
        # Spēles uzsākšana kādai konkrētai daļai
        self.current_game_part = game_part
        if self.start_frame:
            self.start_frame.pack_forget()
        self.canvas = tk.Canvas(self.master, width=1011, height=732)
        self.canvas.pack()

        bg_image_path = f"ekrans{game_part}.png"
        self.bg_image = ImageTk.PhotoImage(file=bg_image_path)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image)

        if game_part <= 4:
            self.setup_game_buttons()
            self.start_timer(lambda: self.end_game(game_part), 30000)
        else:
            self.found_numbers = set()
            self.periods_needed[game_part - 5] = 1  # Sāk spēles periodu skaitīšanu 
            self.setup_textbox()
            self.start_timer(lambda: self.increment_periods_needed(game_part), 30000)

    def start_timer(self, callback, delay):
        # Taimeri palaišana, lai izsauktu "callback" funkciju pēc norādītās laika
        if self.timer:
            self.master.after_cancel(self.timer)
        self.timer = self.master.after(delay, callback)

    def setup_game_buttons(self):
        # Spēles pogu iestatīšana
        self.buttons = {}
        positions = self.get_positions_for_part(self.current_game_part)
        self.button_images = []

        for i, number in enumerate(range(1, 50)):
            if self.current_game_part == 4:
                image_path = f"ciparu_pogas4/{number}.png"
            else:
                image_path = f"ciparu_pogas/{number}.png"
            img = ImageTk.PhotoImage(Image.open(image_path))
            self.button_images.append(img)
            button = self.canvas.create_image(positions[i][0], positions[i][1], image=img, anchor='nw')
            self.canvas.tag_bind(button, "<Button-1>", lambda event, n=number: self.number_clicked(n))
            self.buttons[number] = button

        self.current_number = 1

    def setup_textbox(self):
        # Tekstloga iestatīšana 5. un 6. daļai
        self.textbox_frame = tk.Frame(self.master)
        self.textbox_frame.pack(side='bottom', fill='x', pady=10)

        self.textbox_label = tk.Label(self.textbox_frame, text="Ieraksti pazudušos ciparus:", font=('Helvetica', 14))
        self.textbox_label.pack(side='left', padx=10)

        self.textbox = tk.Entry(self.textbox_frame, font=('Helvetica', 14))
        self.textbox.pack(side='left', padx=10)

        self.submit_button = tk.Button(self.textbox_frame, text="Ievadīt", command=self.check_number_input, font=('Helvetica', 14))
        self.submit_button.pack(side='left', padx=10)

    def get_positions_for_part(self, part):
        # Iegūt norādītās daļas pogu pozīcijas
        if part in [1, 2]:
            return [(150, 620), (270, 262), (68, 60), (592, 635), (530, 320),
                    (320, 143), (893, 520), (670, 370), (780, 110), (230, 570),
                    (248, 433), (185, 175), (480, 644), (340, 450), (580, 170),
                    (645, 530), (750, 435), (730, 130), (110, 660), (40, 340),
                    (100, 100), (350, 570), (590, 340), (380, 105), (880, 610),
                    (665, 420), (800, 70), (40, 520), (17, 278), (250, 55),
                    (480, 500), (331, 350), (570, 48), (760, 500), (810, 335),
                    (858, 150), (200, 650), (32, 430), (35, 200), (430, 525),
                    (455, 343), (332, 210), (720, 630), (735, 360), (688, 42),
                    (40, 670), (98, 438), (155, 45), (350, 510)]
        elif part == 3:
            return [(150, 620), (270, 262), (68, 60), (592, 635), (533, 318),
                    (325, 146), (893, 520), (670, 370), (780, 110), (230, 570),
                    (248, 433), (185, 175), (480, 644), (340, 450), (580, 173),
                    (645, 530), (750, 435), (730, 130), (110, 660), (40, 340),
                    (100, 100), (350, 570), (593, 340), (380, 105), (880, 610),
                    (665, 420), (800, 70), (40, 520), (17, 278), (250, 55),
                    (480, 506), (331, 354), (570, 48), (760, 502), (810, 335),
                    (858, 150), (200, 650), (32, 433), (35, 200), (430, 525),
                    (457, 346), (332, 210), (720, 630), (735, 360), (688, 42),
                    (40, 670), (98, 438), (155, 45), (350, 510)]
        elif part == 4:
            return [(85, 70), (200, 70), (310, 70), (382, 70), (450, 70), (530, 70), (633, 70), (740, 85), (810, 70), (900, 70),
                    (75, 170), (200, 170), (310, 170), (382, 170), (450, 170), (525, 154), (639, 170), (725, 160), (820, 170), (900, 160),
                    (85, 250), (198, 248), (305, 250), (376, 247), (451, 250), (535, 250), (636, 247), (723, 246), (818, 250), (907, 250),
                    (78, 319), (169, 315), (303, 333), (379, 334), (460, 334), (530, 324), (633, 330), (729, 324), (818, 329), (908, 324),
                    (69, 434), (188, 440), (299, 440), (382, 440), (450, 440), (536, 444), (633, 440), (733, 440), (817, 440)]
        else:
            return []  # Nav pogu pozīciju 5. un 6. daļai

    def number_clicked(self, number):
        # Pogas nospiešanas funkcija 1. līdz 4. spēles daļai
        if number == self.current_number:
            self.last_correct_number_pressed = number
            self.current_number += 1
            x, y = self.canvas.coords(self.buttons[number])
            self.canvas.create_rectangle(x, y, x+20, y+20, fill='green', stipple="gray50")
            print(f"Correct: {number}")
        else:
            print(f"Wrong: {number}")

    def check_textbox_input(self, game_part):
        # Pārbauda 5. un 6. daļas ievadītās vērtības no tekstlodziņa
        input_value = self.textbox.get()
        if input_value.isdigit() and int(input_value) in self.correct_numbers:
            self.found_numbers.add(int(input_value))
            self.show_correct_label()
            if len(self.found_numbers) == 2:
                self.end_game(game_part)
            else:
                self.textbox.delete(0, 'end')
        self.start_timer(lambda: self.increment_periods_needed(game_part), 30000)

    def check_number_input(self):
        # Pārbaudiet teksta logā ievadīto skaitli
        input_value = self.textbox.get()
        if input_value.isdigit() and int(input_value) in self.correct_numbers:
            self.found_numbers.add(int(input_value))
            self.show_correct_label()
            if len(self.found_numbers) == 2:
                self.end_game(self.current_game_part)
            else:
                self.textbox.delete(0, 'end')
        else:
            print(f"Wrong number: {input_value}")
            self.textbox.delete(0, 'end')

    def show_correct_label(self):
        # Ievadot pareizo numuru funcija parāda uzrakstu "Pareizais numurs"
        correct_label = tk.Label(self.textbox_frame, text="Pareizais Numurs", font=('Helvetica', 14), fg='green')
        correct_label.pack(side='left', padx=10)
        self.master.after(2000, correct_label.destroy)

    def increment_periods_needed(self, game_part):
        # Skaita nepieciešamos ciklus spēles soļa pabeigšanai, kas nepieciešami 5. un 6. daļai
        self.periods_needed[game_part - 5] += 1
        self.check_textbox_input(game_part)

    def end_game(self, part):
        # Funkcija izbeidz pašreizējo spēles daļu
        if part <= 4:
            self.best_number_part[part - 1] = self.last_correct_number_pressed
        else:
            self.best_number_part[part - 1] = self.periods_needed[part - 5]
        self.canvas.pack_forget()
        if hasattr(self, 'textbox_frame') and self.textbox_frame:
            self.textbox_frame.pack_forget()
        if self.timer:
            self.master.after_cancel(self.timer)
            self.timer = None
        if part < 6:
            self.intermission_screen(part + 1)
        else:
            self.final_results_screen()

    def intermission_screen(self, next_part):
        # Funkcija rādā starpekrānu daļām nepieciešamo informāciju
        if hasattr(self, 'intermission_frame') and self.intermission_frame:
            self.intermission_frame.pack_forget()

        self.intermission_frame = tk.Frame(self.master)
        self.intermission_frame.pack(fill='both', expand=True)

        custom_message = f"Sāksies nākamā spēles daļa {next_part}\n"
        if next_part == 2:
            custom_message += "Šajā spēles solī pielietosim kārtošanu, lai uzdevumu padarītu vieglāku.\n" "Pirmajā spēles solī numuri no 50 līdz 90 nav nepieciešami mūsu uzdevumam.\n" "Tapēc šos ciparus izņemsim no spēles laukuma.\n" "Tev tiks dotas 30 sekundes, lai atrastu pēc iespējas vairāk skaitļus no 1 līdz 49.\n"
        elif next_part == 3:
            custom_message += "Redzēji uzlabojumu savā spēles rezultātā?\n" "Tagad uz spēles laukuma tiks uzstādīts 3 x 3 režģis.\n" "Kas izmanto soli 'Ieviest kārtību'.\n" "Numuri ir sakārtoti tā ka numurs 1 atrodas kreisajā apakšējā stūrī un cipari iet no apakšas uz augšu,\n un no kreisās puses uz labo.\n" "Piemērs: Cipars 1 ir kreisajā apakšējā kvadrātā. Cipars 2 ir kreisajā vidējā kvadrātā.\n" "Cipars 3 ir kreisajā augšējā kvadrātā. Cipars 4 ir vidējā apakšējā kvadrātā u.t.t.\n" "Tev tiks dotas 30 sekundes, lai atrastu pēc iespējas vairāk skaitļus no 1 līdz 49.\n"
        elif next_part == 4:
            custom_message += "Redzēji vēl lielāku uzlabojumu savā spēles rezultātā?\n" "Tagad implementēsim 'Standartizēšanu'.\n" "Šajā spēles solī spēles laukums izskatīsies krietni savādāk ar precīzāku skatiļu kārtošanas sistēmu.\n" "Šādā veidā ļaujot skaitļus sakārtot spēlētājam pazīstāmākā veidā jeb standartiski.\n" "Tev tiks dotas 30 sekundes, lai atrastu pēc iespējas vairāk skaitļus no 1 līdz 49.\n"
        elif next_part == 5:
            custom_message += "Vai redzēji labāku sniegumu savā spēles rezultātā?\n" "Tagad sākot nākamo spēles soli tavs uzdevums būs atrast 2 trūkstošos skaitļus\n un tos ierakstīt un ievadīt paredzētajā vietā.\n" "Bet tiks skaitīts cik 30 sekundžu cikli ir nepieciešami spēlētājam,\n lai atrastu abus trūkstošos skaitļus.\n" "Spēle solis beidzas, kad abi skaitļi ir atrasti.\n"
        elif next_part == 6:
            custom_message += "Kāds bija tavas sajūtas tagad par tavu spēles rezultātu?\n" "Tagad simulēsim situāciju, kad darba vidē ir implementēta:\n Kārtošanas, Kārtības ieviešana un Standartizēšana.\n" "Sākot nākamo spēles soli tavs uzdevums būs atrast 2 trūkstošos skaitļus\n un tos ierakstīt un ievadīt paredzētajā vietā.\n" "Tiks skaitīts cik 30 sekundžu cikli ir nepieciešami spēlētājam, lai atrastu abus trūkstošos skaitļus.\n"

        result_label = tk.Label(self.intermission_frame, text=f"{next_part - 1} Spēles daļas rezultāts: {self.best_number_part[next_part - 2]}\n{custom_message}Spied 'Turpināt', lai sāktu nākamo spēles soli.",
                                font=('Helvetica', 18))
        result_label.pack(pady=20)

        continue_button = tk.Button(self.intermission_frame, text="Turpināt", 
                                    command=lambda: self.clear_intermission_and_continue(next_part), 
                                    font=('Helvetica', 18))
        continue_button.pack(pady=20)

    def clear_intermission_and_continue(self, next_part):
        # Notīriet starpekrānu un pāreiet uz nākamās daļas
        if hasattr(self, 'intermission_frame') and self.intermission_frame:
            self.intermission_frame.pack_forget()
        self.setup_game(next_part)

    def final_results_screen(self):
        # funcija izvada gala rezultātu ekrānu
        if hasattr(self, 'final_results_frame') and self.final_results_frame:
            self.final_results_frame.pack_forget()

        self.final_results_frame = tk.Frame(self.master)
        self.final_results_frame.pack(fill='both', expand=True)

        results_label = tk.Label(self.final_results_frame, text=f"Kādas ir tavas atziņas par šo soļu implemetēšanu darba vidē, lai uzdevumus padarītu vieglākus un ātrākus.\n Spēles rezultāti:\n Pirmās daļas pēdējais atzīmētais cipars: {self.best_number_part[0]}\n Otrās daļas pēdējais atzīmētais cipars: {self.best_number_part[1]}\n Trešās daļas pēdējais atzīmētais cipars: {self.best_number_part[2]}\n Ceturtās daļas pēdējais atzīmētais cipars: {self.best_number_part[3]}\n Piektās daļas nepieciešami 30 sekundžu cikli: {self.periods_needed[0]}\n Sestās daļas nepieciešami 30 sekundžu cikli: {self.periods_needed[1]}",
                                 font=('Helvetica', 20))
        results_label.pack(pady=20)

        restart_button = tk.Button(self.final_results_frame, text="Sākt spēli no jauna", command=self.restart_game, font=('Helvetica', 18))
        restart_button.pack(pady=20)

    def restart_game(self):
        # Funkcija sāk spēli no sākuma
        self.final_results_frame.pack_forget()
        self.start_frame.pack(fill='both', expand=True)
        self.best_number_part = [None, None, None, None, None, None]
        self.periods_needed = [0, 0]
        self.current_game_part = 1

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGameApp(root)
    root.mainloop()
