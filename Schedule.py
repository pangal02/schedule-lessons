import os
import datetime


def main():
    # Λίστα με τις ημέρες από Δευτέρα έως Παρασκευή
    days = ["ΔΕΥΤΕΡΑ", "ΤΡΙΤΗ", "ΤΕΤΑΡΤΗ", "ΠΕΜΠΤΗ", "ΠΑΡΑΣΚΕΥΗ"]

    # Κενό λεξικό για το πρόγραμμα μαθημάτων
    schedule = {}
    print("\n📚 Καλώς ήρθατε στο Πρόγραμμα Μαθημάτων!\n")
    # Φόρτωμα του προγράμματος και επιστροφή της τελευταίας ημερομηνίας και ώρας αποθήκευσης
    last_saved_date_time = load_schedule(schedule)
    if last_saved_date_time:
        print(f"📚 Το πρόγραμμα μαθημάτων είναι έτοιμο, τελευταία αποθήκευση: {last_saved_date_time}")

    # Αρχική κατάσταση χωρίς αποθήκευση
    current_changes = False

    choice = -1 
    while True:
        menu()
        choice = input().strip()
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
        elif choice == "5":
            save_schedule(schedule)
            current_changes = False # Δεν υπάρχουν αλλαγές μετά την αποθήκευση
        elif choice == "6":
            delete_all_schedule(schedule)  # Κλήση της συνάρτησης διαγραφής
            current_changes = False # Δεν υπάρχει κάτι για αποθήκευση
        elif choice == "7":
            if current_changes:
                print("⚠️ Υπάρχουν αλλαγές που δεν έχουν αποθηκευτεί.")
                save = input("Θέλετε να αποθηκεύσετε το πρόγραμμα πριν κλείσετε; (ναι/οχι): ").strip().lower()
                while save not in ["ναι","οχι"]:
                    save = input("⚠️ Παρακαλώ απαντήστε μόνο με 'ναι' ή 'οχι': ").strip().lower()
                if save == "ναι":
                    save_schedule(schedule)
            print("Το πρόγραμμα τερματίστηκε.")
            break
        else :
            print("Παρακαλώ επιλέξτε μια από τις επιλογές [1-6].")
# Τελος Main

def menu():
    print("\nΕπιλέξτε μια από τις παρακάτω επιλογές:")
    print("1. Εισαγωγή Προγράμματος Μαθημάτων")
    print("2. Αναζήτηση Μαθήματος")
    print("2. Επεξεργασία Προγράμματος Μαθημάτων")
    print("3. Εμφάνιση Προγράμματος Μαθημάτων")
    print("4. Αποθήκευση")
    print("5. Διαγραφή Όλου του Προγράμματος")
    print("6. Έξοδος")
    print("Επιλογή: ", end="")
# Τέλος Menu


def load_schedule(schedule):
    if os.path.exists("schedule.txt"):
        with open("schedule.txt", "r") as file:
            lines = file.readlines()
            date_time_line = lines[0].strip()
            last_saved_date_time = date_time_line.split(": ")[1]  # Παίρνουμε την τελευταία ημερομηνία και ώρα αποθήκευσης
            print(f"📚 Το πρόγραμμα μαθημάτων φορτώθηκε επιτυχώς! Τελευταία αποθήκευση: {last_saved_date_time}")

            for line in lines[1:]:
                day, lessons = line.strip().split(": ")
                schedule[day] = lessons.split(", ")

            return last_saved_date_time
    else:
        print("⚠️ Δεν βρέθηκε προηγούμενο αρχείο προγράμματος.")
        return None
# Τελος Load_Schedule


def make_list(days, schedule):  # Προσθέτουμε το schedule ως παράμετρο
    # Για κάθε ημέρα, ρωτάμε τον χρήστη να προσθέσει μαθήματα
    for day in days:
        schedule[day] = []  # Δημιουργούμε μια κενή λίστα για την ημέρα

        print(f"\n📅 Προσθήκη μαθημάτων για {day}:")
    
        while True:
            lesson = input("Προσθέστε ένα μάθημα (ή πατήστε Enter για να προχωρήσετε): ").strip()
        
            if lesson == "":  # Αν ο χρήστης δεν έγραψε τίποτα
                while True:
                    if day == days[-1]:  # Αν έχουμε φτάσει στην Παρασκευή
                        next_day = input("Θέλετε να ολοκληρώσετε το πρόγραμμα; (ναι/οχι): ").strip().lower()
                    else:
                        next_day = input("Θέλετε να προχωρήσετε στην επόμενη ημέρα; (ναι/οχι): ").strip().lower()
                    if next_day in ["ναι", "οχι"]:
                        break
                    print("⚠️ Παρακαλώ απαντήστε μόνο με 'ναι' ή 'οχι'.")

                if next_day == "ναι":
                    break  # Πάμε στην επόμενη ημέρα
                else:
                    continue  # Ξαναζητάμε μάθημα για την ίδια ημέρα

            schedule[day].append(lesson)  # Προσθήκη του μαθήματος στη λίστα
            date = datetime.datetime.now()

            # 📌 Εκτύπωση του προγράμματος της ημέρας μετά από κάθε προσθήκη
            print(f"📜 Πρόγραμμα {day} --> {', '.join(schedule[day])}")
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
        print(f"Τρέχον πρόγραμμα για την {day}: {', '.join(schedule[day])}")
        print("Πατήστε 'Π' για να προσθέσετε ένα μάθημα ή 'Δ' για να διαγράψετε ένα μάθημα.")
        choice = input().strip().upper()
        if choice == "Π":
            lesson = input("Προσθέστε ένα μάθημα: ").strip()
            if lesson not in schedule[day]:
                schedule[day].append(lesson)
            else:
                print("⚠️ Το μάθημα υπάρχει ήδη στο πρόγραμμα!")
        elif choice == "Δ":
            lesson = input("Διαγράψτε ένα μάθημα: ").strip()
            if lesson in schedule[day]:
                schedule[day].remove(lesson)
            else:
                print("⚠️ Το μάθημα δεν υπάρχει στο πρόγραμμα!")
        else:
            print("⚠️ Μη έγκυρη επιλογή.")
        print(f"Νέο πρόγραμμα για την {day}: {', '.join(schedule[day])}")
        next_day = input("Θέλετε να επεξεργαστείτε κι άλλη ημέρα; (ναι/οχι): ").strip().lower()
        while next_day not in ["ναι", "οχι"]:
            next_day = input("⚠️ Παρακαλώ απαντήστε μόνο με 'ναι' ή 'οχι': ").strip().lower()
        if next_day == "οχι":
            break
# Τελος Update_Schedule

def search_lesson(schedule):
    if not schedule:
        print("⚠️ Το πρόγραμμα είναι άδειο. Προσθέστε πρώτα μαθήματα.")
        return
    lesson = input("Αναζήτηση μαθήματος: ").strip().lower()
    found = False
    for day, lessons in schedule.items():
        for l in lessons:
            if lesson in l.lower():
                print(f"🔍 Το μάθημα '{l}' βρίσκεται στην {day}.")
                found = True
    if not found:
        print(f"⚠️ Το μάθημα '{lesson}' δεν βρέθηκε στο πρόγραμμα.")


def delete_all_schedule(schedule):
    if not schedule:
        print("⚠️ Το πρόγραμμα είναι ήδη άδειο.")
        return
    # Ερωτάμε τον χρήστη αν είναι σίγουρος για τη διαγραφή
    confirmation = input("Είστε σίγουροι ότι θέλετε να διαγράψετε όλο το πρόγραμμα μαθημάτων; (ναι/οχι): ").strip().lower()
    while confirmation not in ["ναι", "οχι"]:
        confirmation = input("⚠️ Παρακαλώ απαντήστε μόνο με 'ναι' ή 'οχι': ").strip().lower()

    if confirmation == "ναι":
        schedule.clear()  # Διαγράφουμε όλο το λεξικό
        print("✅ Το πρόγραμμα μαθημάτων διαγράφηκε επιτυχώς.")
    else:
        print("⚠️ Η διαγραφή ακυρώθηκε.")
# Τελος Delete_All_Schedule


# Αποθήκευση του προγράμματος σε ένα αρχείο
def save_schedule(schedule):
    # Παίρνουμε την τρέχουσα ημερομηνία και ώρα σε μορφή dd/mm/yyyy HH:MM:SS
    now = datetime.datetime.now()
    date_time = now.strftime('%d/%m/%Y %H:%M:%S')
    with open("schedule.txt", "w") as file:
        file.write(f"Τελευταία Αποθήκευση: {date_time}\n")   # Αποθηκεύουμε την ημερομηνία & ώρα αποθήκευσης
        for day, lessons in schedule.items():
            file.write(f"{day}: {', '.join(lessons)}\n")
    print(f"📂 Το πρόγραμμα αποθηκεύτηκε στο 'schedule.txt' στις {date_time}.")

# Τελος Save_Schedule

def print_schedule(schedule):
    if not schedule:
        print("⚠️ Το πρόγραμμα είναι άδειο. Προσθέστε πρώτα μαθήματα.")
        return
    # Εμφάνιση του τελικού προγράμματος
    print("\n📅 Τελικό Πρόγραμμα Μαθημάτων:")
    for day, lessons in schedule.items():
        if lessons:
            print(f"{day}: {', '.join(lessons)}")
        else:
            print(f"{day}: -")
# Τελος Print


# Καλούμε την main για να ξεκινήσει το πρόγραμμα
main()