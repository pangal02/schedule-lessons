import os
import datetime
import msvcrt
import re


FOLDER_PATH = os.path.join(os.getcwd(), "save")
FILE_PATH = os.path.join(FOLDER_PATH, "schedule.txt")

def main():
    # Καθορίζουμε το μονοπάτι για το φάκελο και το αρχείο

    # Λίστα με τις ημέρες από Δευτέρα έως Παρασκευή
    days = ("ΔΕΥΤΕΡΑ", "ΤΡΙΤΗ", "ΤΕΤΑΡΤΗ", "ΠΕΜΠΤΗ", "ΠΑΡΑΣΚΕΥΗ")

    # Κενό λεξικό για το πρόγραμμα μαθημάτων
    schedule = {}
    print("\n📚 Καλώς ήρθατε στο Πρόγραμμα Μαθημάτων!\n")
    # Φόρτωμα του προγράμματος και επιστροφή της τελευταίας ημερομηνίας και ώρας αποθήκευσης
    last_saved_date_time = load_schedule(schedule)
    # Αρχική κατάσταση χωρίς αποθήκευση
    current_changes = False

    choice = -1
    while True:
        menu()
        choice = input("Επιλογή: ").strip()
        if choice == "1":
            make_list(days, schedule)
            current_changes = True  # Αλλαγές στο πρόγραμμα
        elif choice == "2":
            search_lesson(schedule)
        elif choice == "3":
            update_schedule(schedule)
            current_changes = True  # Αλλαγές στο πρόγραμμα
        elif choice == "4":
            print_schedule(schedule)
            input("\nΠατήστε Enter για να συνεχίσετε...")
        elif choice == "5":
            save_schedule(schedule)
            current_changes = False # Δεν υπάρχουν αλλαγές μετά την αποθήκευση
        elif choice == "6":
            delete_all_schedule(schedule)  # Κλήση της συνάρτησης διαγραφής
            current_changes = False # Δεν υπάρχει κάτι για αποθήκευση
        elif choice == "7":
            if current_changes:
                print("⚠️ Υπάρχουν αλλαγές που δεν έχουν αποθηκευτεί.")
                save = get_choice("Θέλετε να αποθηκεύσετε το πρόγραμμα πριν κλείσετε; (ν/ο): ")
                if save == "ν":
                    save_schedule(schedule)
            print("Το πρόγραμμα τερματίστηκε.")
            break
        else:
            print("Παρακαλώ επιλέξτε μια από τις επιλογές [1-7].")
# Τελος Main

def menu():
    print()
    print("=" * 70)
    print("Επιλέξτε μια από τις παρακάτω επιλογές:")
    print("1. Εισαγωγή Προγράμματος Μαθημάτων")
    print("2. Αναζήτηση Μαθήματος")
    print("3. Επεξεργασία Προγράμματος Μαθημάτων")
    print("4. Εμφάνιση Προγράμματος Μαθημάτων")
    print("5. Αποθήκευση")
    print("6. Διαγραφή Όλου του Προγράμματος")
    print("7. Έξοδος")
# Τέλος Menu

def load_schedule(schedule):
    if not os.path.exists(FILE_PATH):
        print("⚠️ Δεν βρέθηκε προηγούμενο αρχείο προγράμματος.")
        return None

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]  # Αφαιρούμε κενές γραμμές

            if not lines:
                print("⚠️ Το αρχείο είναι άδειο!")
                return None

            if not lines[0].startswith("Τελευταία Αποθήκευση: "):
                print("⚠️ Το αρχείο έχει λανθασμένη μορφή! Παράλειψη φόρτωσης.")
                return None

            last_saved_date_time = lines[0].split(": ", 1)[1]  
            print(f"📚 Το πρόγραμμα μαθημάτων φορτώθηκε επιτυχώς! Τελευταία αποθήκευση: {last_saved_date_time}")

            for line in lines[1:]:  # Ξεκινάμε από τη 2η γραμμή
                if ": " not in line:
                    continue
                day, lessons = line.split(": ", 1)
                print(f"HMERA: {day} ")
                lessons_dict = {}

                if lessons:
                    for lesson in lessons.split(", "):
                        if " @ " not in lesson and lesson != "-":
                            print(f"⚠️ Σφάλμα στη γραμμή: {lesson}. Λέιπει το '@'.")
                            continue
                        lesson_name, lesson_time = lesson.split(" @ ", 1)
                        lessons_dict[lesson_name.strip()] = lesson_time.strip()
                
                schedule[day.strip()] = lessons_dict

            return last_saved_date_time
    except Exception as e:
        print(f"⚠️ Σφάλμα κατά το άνοιγμα του αρχείου: {e}")
        return None

# Τελος Load_Schedule

def is_valid_time_format(time):
    return re.match(r"^\d{2}:\d{2}-\d{2}:\d{2}$", time)
# Τελος Is_Valid_Time_Format


def make_list(days, schedule):  
    for day in days:
        schedule[day] = {}  

        print(f"\n📅 Προσθήκη μαθημάτων για {day}:")
    
        while True:
            lesson = input("Προσθέστε ένα μάθημα (ή πατήστε Enter για να προχωρήσετε): ").strip()
            if lesson == "":  
                next_day = get_choice("Θέλετε να προχωρήσετε στην επόμενη ημέρα; (ν/ο): ").strip().lower()
                if next_day == "ν":
                    break  
                else:
                    continue  

            while True:
                lesson_time = input("Προσθέστε την ώρα του μαθήματος (π.χ. 10:00-11:00): ").strip()
                if is_valid_time_format(lesson_time):
                    break
                print("⚠️ Η ώρα δεν είναι στη σωστή μορφή! Παράδειγμα: 10:00-11:00")

            schedule[day][lesson] = lesson_time  
            print(f"📜 Πρόγραμμα {day} --> {lesson} @ {lesson_time}")

# Τελος Make_List

def update_schedule(schedule):
    if not schedule:
        print("⚠️ Το πρόγραμμα είναι άδειο. Προσθέστε πρώτα μαθήματα.")
        return
    # Επεξεργασία του προγράμματος
    while True:
        day = input("Επιλέξτε ημέρα για επεξεργασία: ").strip().upper()
        if day not in schedule:
            print("⚠️ Η ημέρα δεν υπάρχει στο πρόγραμμα.")
            continue
        print(f"Τρέχον πρόγραμμα για την {day}:")
        for lesson, time in schedule[day].items():
            print(f"{lesson} @ {time}")
        print("Πατήστε 'Π' για να προσθέσετε ένα μάθημα ή 'Δ' για να διαγράψετε ένα μάθημα.")
        choice = input().strip().upper()
        if choice == "Π":
            lesson = input("Προσθέστε ένα μάθημα: ").strip()
            lesson_time = input("Προσθέστε την ώρα του μαθήματος (π.χ. 10:00-11:00): ").strip()
            if lesson not in schedule[day]:
                schedule[day][lesson] = lesson_time
            else:
                print("⚠️ Το μάθημα υπάρχει ήδη στο πρόγραμμα!")
        elif choice == "Δ":
            lesson = input("Διαγράψτε ένα μάθημα: ").strip()
            if lesson in schedule[day]:
                del schedule[day][lesson]
            else:
                print("⚠️ Το μάθημα δεν υπάρχει στο πρόγραμμα!")
        else:
            print("⚠️ Μη έγκυρη επιλογή.")
        print(f"Νέο πρόγραμμα για την {day}:")
        for lesson, time in schedule[day].items():
            print(f"{lesson} @ {time}")
        next_day = get_choice("Θέλετε να επεξεργαστείτε κι άλλη ημέρα; (ν/ο): ")
        if next_day == "ο":
            break
# Τελος Update_Schedule

def search_lesson(schedule):
    if not schedule:
        print("⚠️ Το πρόγραμμα είναι άδειο. Προσθέστε πρώτα μαθήματα.")
        return

    lesson_query = input("Αναζήτηση μαθήματος: ").strip().lower()
    results = []

    for day, lessons in schedule.items():
        for lesson, time in lessons.items():
            if lesson_query in lesson.lower():
                results.append(f"🔍 {lesson} βρίσκεται στην {day} στις {time}.")

    if results:
        print("\n".join(results))
    else:
        print(f"⚠️ Το μάθημα '{lesson_query}' δεν βρέθηκε στο πρόγραμμα.")
# Τελος Search_Lesson

def delete_all_schedule(schedule):
    if not schedule:
        print("⚠️ Το πρόγραμμα είναι ήδη άδειο.")
        return
    # Ερωτάμε τον χρήστη αν είναι σίγουρος για τη διαγραφή
    confirmation = get_choice("Είστε σίγουροι ότι θέλετε να διαγράψετε όλο το πρόγραμμα μαθημάτων; (ν/ο): ")
    if confirmation == "ν":
        schedule.clear()  # Διαγράφουμε όλο το λεξικό
        print("✅ Το πρόγραμμα μαθημάτων διαγράφηκε επιτυχώς.")
    else:
        print("⚠️ Η διαγραφή ακυρώθηκε.")
# Τελος Delete_All_Schedule

def save_schedule(schedule):
    # Παίρνουμε την τρέχουσα ημερομηνία και ώρα σε μορφή dd/mm/yyyy HH:MM:SS
    now = datetime.datetime.now()
    date_time = now.strftime('%d/%m/%Y %H:%M:%S')

    # Ελέγχουμε αν ο φάκελος υπάρχει, αν όχι τον δημιουργούμε
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        file.write(f"Τελευταία Αποθήκευση: {date_time}\n")   # Αποθηκεύουμε την ημερομηνία & ώρα αποθήκευσης
        for day, lessons in schedule.items():
            sorted_lessons = sorted(lessons.items(), key=lambda x: x[1])  # Ταξινόμηση με βάση την ώρα
            lessons_str = ", ".join([f"{lesson} @ {time}" for lesson, time in sorted_lessons])
            file.write(f"{day}: {lessons_str}\n")
    print(f"📂 Το πρόγραμμα αποθηκεύτηκε στο 'schedule.txt' στις {date_time}.")
# Τελος Save_Schedule

def print_schedule(schedule):
    if not schedule:
        print("⚠️ Το πρόγραμμα είναι άδειο. Προσθέστε πρώτα μαθήματα.")
        return
    # Εμφάνιση του τελικού προγράμματος
    print("\n📅 Τελικό Πρόγραμμα Μαθημάτων:")
    print("=" * 70)
    for day, lessons in schedule.items():
        if lessons:
            sorted_lessons = sorted(lessons.items(), key=lambda x: x[1])  # Ταξινόμηση με βάση την ώρα
            for lesson, time in sorted_lessons:
                print(f"{day}: {lesson} @ {time}")

            print("-" * 70)
        else:
            print(f"{day}: -- Χωρίς Μαθήματα --")
    print("=" * 70)
# Τελος Print

def get_choice(prompt):
    print(prompt, end="", flush=True)
    while True:
        choice = msvcrt.getwch().lower()
        if choice in ["ν", "ο"]:
            print()
            return choice
# Τελος Get_Choice

# Καλούμε την main για να ξεκινήσει το πρόγραμμα
main()