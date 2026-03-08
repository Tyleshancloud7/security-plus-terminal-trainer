import json
import os
import random
import signal
import textwrap
from datetime import datetime, date

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
PINK = "\033[95m"
HOT_PINK = "\033[38;5;213m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"

DATA_FILE = "security_plus_progress.json"

DOMAIN_1 = [
    {"question": "What does CIA stand for?", "answer": "confidentiality integrity availability", "hint": "Core security principles."},
    {"question": "What does AAA stand for?", "answer": "authentication authorization accounting", "hint": "Access control model."},
    {"question": "What does MFA stand for?", "answer": "multi factor authentication", "hint": "More than one factor."},
    {"question": "What type of control is a firewall?", "answer": "preventive", "hint": "Stops attacks before they happen."},
    {"question": "What category of control is a firewall?", "answer": "technical", "hint": "Implemented through technology."},
    {"question": "What category of control is a security policy?", "answer": "administrative", "hint": "Management-driven."},
    {"question": "What category of control is a door lock?", "answer": "physical", "hint": "Think building access."},
    {"question": "What type of control is a backup restore process?", "answer": "corrective", "hint": "Used after something goes wrong."},
    {"question": "What type of control is a warning banner?", "answer": "deterrent", "hint": "Discourages bad behavior."},
    {"question": "What type of control is a security awareness policy?", "answer": "directive", "hint": "Tells users what to do."},
    {"question": "What type of control replaces a primary control when that control is not possible?", "answer": "compensating", "hint": "A substitute control."},
]

DOMAIN_2 = [
    {"question": "Phishing is what type of attack?", "answer": "social engineering", "hint": "Manipulating people."},
    {"question": "Ransomware is what type of threat?", "answer": "malware", "hint": "Malicious software."},
    {"question": "An attacker intercepting communication between two parties is what attack?", "answer": "man in the middle", "hint": "MITM."},
    {"question": "A flood of traffic meant to overwhelm a service is what attack?", "answer": "ddos", "hint": "Distributed denial of service."},
    {"question": "A text-message phishing attack is called what?", "answer": "smishing", "hint": "SMS phishing."},
    {"question": "A phone-call phishing attack is called what?", "answer": "vishing", "hint": "Voice phishing."},
    {"question": "Scanning open ports is what attack stage?", "answer": "reconnaissance", "hint": "Information gathering."},
    {"question": "Moving from one system to another after compromise is called what?", "answer": "lateral movement", "hint": "Moving within the environment."},
    {"question": "Malicious code disguised as legitimate software is called what?", "answer": "trojan", "hint": "Looks harmless, but isn't."},
]

DOMAIN_3 = [
    {"question": "What port does HTTP use?", "answer": "80", "hint": "Web traffic, not secure."},
    {"question": "What port does HTTPS use?", "answer": "443", "hint": "Secure web traffic."},
    {"question": "What port does SSH use?", "answer": "22", "hint": "Secure shell."},
    {"question": "What port does FTP use?", "answer": "21", "hint": "File transfer."},
    {"question": "What port does SMTP use?", "answer": "25", "hint": "Mail sending."},
    {"question": "What port does DNS use?", "answer": "53", "hint": "Name resolution."},
    {"question": "What port does RDP use?", "answer": "3389", "hint": "Remote Desktop."},
    {"question": "What does IDS stand for?", "answer": "intrusion detection system", "hint": "Detects suspicious traffic."},
    {"question": "What does IPS stand for?", "answer": "intrusion prevention system", "hint": "Detects and blocks."},
    {"question": "What network zone often hosts public-facing servers?", "answer": "dmz", "hint": "Between internet and internal network."},
    {"question": "What kind of encryption uses one shared key?", "answer": "symmetric", "hint": "Same key to encrypt and decrypt."},
    {"question": "What kind of encryption uses a public and private key?", "answer": "asymmetric", "hint": "Two different keys."},
]

DOMAIN_4 = [
    {"question": "What does PICERL stand for?", "answer": "preparation identification containment eradication recovery lessons learned", "hint": "Incident response lifecycle."},
    {"question": "What is the first step in PICERL?", "answer": "preparation", "hint": "Before the incident happens."},
    {"question": "What comes after Identification in PICERL?", "answer": "containment", "hint": "Stop the spread."},
    {"question": "What comes after Containment in PICERL?", "answer": "eradication", "hint": "Remove the threat."},
    {"question": "What comes after Eradication in PICERL?", "answer": "recovery", "hint": "Restore operations."},
    {"question": "What is the final step in PICERL?", "answer": "lessons learned", "hint": "Review and improve."},
    {"question": "What does SIEM stand for?", "answer": "security information and event management", "hint": "Centralized logging and alerting."},
    {"question": "What does EDR stand for?", "answer": "endpoint detection and response", "hint": "Endpoint monitoring and response."},
]

DOMAIN_5 = [
    {"question": "What risk response uses cyber insurance?", "answer": "transfer", "hint": "Move the financial burden."},
    {"question": "What risk response means reducing the likelihood or impact?", "answer": "mitigate", "hint": "Lower the risk."},
    {"question": "What risk response means not doing the risky activity?", "answer": "avoid", "hint": "Do not engage."},
    {"question": "What risk response means acknowledging the risk and doing nothing further?", "answer": "accept", "hint": "Live with it."},
    {"question": "What does DLP stand for?", "answer": "data loss prevention", "hint": "Stops sensitive data from leaving."},
    {"question": "Policies, standards, procedures, and guidelines belong to what area?", "answer": "governance", "hint": "Rules and oversight."},
    {"question": "What acronym helps remember risk responses: Mitigate, Accept, Avoid, Transfer?", "answer": "maat", "hint": "Four letters."},
]

FLASHCARDS = [
    ("CIA", "Confidentiality, Integrity, Availability"),
    ("AAA", "Authentication, Authorization, Accounting"),
    ("MFA", "Multi-Factor Authentication"),
    ("PICERL", "Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned"),
    ("MAAT", "Mitigate, Accept, Avoid, Transfer"),
    ("Firewall", "Preventive technical control"),
    ("Door lock", "Physical control"),
    ("SIEM", "Security Information and Event Management"),
    ("HTTPS", "Port 443"),
    ("SSH", "Port 22"),
    ("RDP", "Port 3389"),
    ("DMZ", "Perimeter network for public-facing systems"),
]

QUIZ_GROUPS = {
    "1": ("Domain 1 - Security Concepts", DOMAIN_1),
    "2": ("Domain 2 - Threats and Vulnerabilities", DOMAIN_2),
    "3": ("Domain 3 - Architecture and Design", DOMAIN_3),
    "4": ("Domain 4 - Security Operations", DOMAIN_4),
    "5": ("Domain 5 - Governance and Risk", DOMAIN_5),
}

def default_progress():
    return {
        "total_quizzes": 0,
        "best_score": 0,
        "last_study_date": "",
        "streak": 0,
        "missed_questions": [],
        "quiz_history": []
    }

def load_progress():
    if not os.path.exists(DATA_FILE):
        return default_progress()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default_progress()

def save_progress(progress):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)

def clear_screen():
    os.system("clear")

def print_header(title):
    print(HOT_PINK + BOLD + "═" * 68 + RESET)
    print(HOT_PINK + BOLD + title.center(68) + RESET)
    print(HOT_PINK + BOLD + "═" * 68 + RESET)

def pause():
    input(YELLOW + "\nPress Enter to continue..." + RESET)

def normalize(text):
    cleaned = text.lower().strip()
    for char in [",", ".", "!", "?", "-", "_", ":", ";", "/", "\\", "(", ")"]:
        cleaned = cleaned.replace(char, " ")
    return " ".join(cleaned.split())

def is_correct(user_answer, correct_answer):
    user_norm = normalize(user_answer)
    correct_norm = normalize(correct_answer)
    if user_norm == correct_norm:
        return True
    return set(user_norm.split()) == set(correct_norm.split())

def timeout_handler(signum, frame):
    raise TimeoutError

def timed_input(prompt, seconds):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        answer = input(prompt)
        signal.alarm(0)
        return answer
    except TimeoutError:
        signal.alarm(0)
        return None

def update_streak(progress):
    today = date.today()
    last = progress.get("last_study_date", "")

    if not last:
        progress["streak"] = 1
    else:
        last_date = datetime.strptime(last, "%Y-%m-%d").date()
        diff = (today - last_date).days
        if diff == 0:
            pass
        elif diff == 1:
            progress["streak"] += 1
        else:
            progress["streak"] = 1

    progress["last_study_date"] = today.strftime("%Y-%m-%d")

def add_missed_question(progress, item):
    existing_questions = {q["question"] for q in progress["missed_questions"]}
    if item["question"] not in existing_questions:
        progress["missed_questions"].append(item)

def remove_missed_question(progress, item):
    progress["missed_questions"] = [
        q for q in progress["missed_questions"]
        if q["question"] != item["question"]
    ]

def show_banner():
    clear_screen()
    print(HOT_PINK + BOLD + r"""
   ______                      _ __        __   ____ 
  / ____/___  _______  _______(_) /___  __/ /_ / __ \
 / /   / __ \/ ___/ / / / ___/ / __/ / / / __// / / /
/ /___/ /_/ / /  / /_/ (__  ) / /_/ /_/ / /_ / /_/ / 
\____/\____/_/   \__,_/____/_/\__/\__,_/\__(_)____/  
                                                      
   SECURITY+ TERMINAL STUDY APP V3  •  MAC EDITION
""" + RESET)

def show_stats(progress):
    print(CYAN + f"Study streak: {progress['streak']} day(s)" + RESET)
    print(CYAN + f"Total quizzes completed: {progress['total_quizzes']}" + RESET)
    print(CYAN + f"Best score: {progress['best_score']}%" + RESET)
    print(CYAN + f"Saved missed questions: {len(progress['missed_questions'])}" + RESET)
    print(DIM + f"Progress file: {DATA_FILE}" + RESET)

def show_memory_sheet():
    clear_screen()
    print_header("SECURITY+ MEMORY SHEET")
    print(CYAN + """
CIA     = Confidentiality, Integrity, Availability
AAA     = Authentication, Authorization, Accounting
MFA     = Multi-Factor Authentication
PICERL  = Preparation, Identification, Containment, Eradication,
          Recovery, Lessons Learned
MAAT    = Mitigate, Accept, Avoid, Transfer

Ports:
HTTP    = 80
HTTPS   = 443
SSH     = 22
FTP     = 21
SMTP    = 25
DNS     = 53
RDP     = 3389

Controls:
Preventive / Detective / Corrective / Deterrent / Directive / Compensating

Categories:
Administrative / Technical / Physical
""" + RESET)
    pause()

def show_flashcards():
    cards = FLASHCARDS[:]
    random.shuffle(cards)

    for term, definition in cards:
        clear_screen()
        print_header("FLASHCARD MODE")
        print(PINK + BOLD + f"\nTERM: {term}\n" + RESET)
        command = input("Press Enter to flip, or type q to quit: ").strip().lower()
        if command == "q":
            return
        print(GREEN + textwrap.fill(f"DEFINITION: {definition}", width=68) + RESET)
        command = input("\nPress Enter for next, or type q to quit: ").strip().lower()
        if command == "q":
            return

def show_history(progress):
    clear_screen()
    print_header("QUIZ HISTORY")

    history = progress.get("quiz_history", [])
    if not history:
        print(YELLOW + "No quiz history yet." + RESET)
        pause()
        return

    for entry in history[-10:]:
        print(f"{GREEN}{entry['date']}{RESET} | "
              f"{CYAN}{entry['quiz_name']}{RESET} | "
              f"{PINK}{entry['score']}/{entry['total']}{RESET} | "
              f"{YELLOW}{entry['percent']}%{RESET}")
    pause()

def run_quiz(progress, quiz_name, question_bank, round_size=None, timed=False, seconds=15):
    questions = question_bank[:]
    random.shuffle(questions)

    if round_size is not None:
        questions = questions[:round_size]

    score = 0
    local_missed = []

    update_streak(progress)

    for idx, item in enumerate(questions, start=1):
        clear_screen()
        print_header(quiz_name)
        print(CYAN + f"Question {idx} of {len(questions)}" + RESET)
        print(BLUE + "─" * 68 + RESET)
        print(textwrap.fill(item["question"], width=68))
        print(BLUE + "─" * 68 + RESET)

        if timed:
            print(YELLOW + f"You have {seconds} seconds." + RESET)
            answer = timed_input("Your answer ('hint' or 'skip'): ", seconds)
            if answer is None:
                print(RED + "\nTime's up!" + RESET)
                local_missed.append(item)
                add_missed_question(progress, item)
                pause()
                continue
        else:
            answer = input("Your answer ('hint' or 'skip'): ")

        if normalize(answer) == "hint":
            print(YELLOW + f"Hint: {item['hint']}" + RESET)
            answer = input("Your answer: ")

        if normalize(answer) == "skip":
            print(RED + f"Skipped. Correct answer: {item['answer']}" + RESET)
            local_missed.append(item)
            add_missed_question(progress, item)
            pause()
            continue

        if is_correct(answer, item["answer"]):
            print(GREEN + "Correct!" + RESET)
            score += 1
            remove_missed_question(progress, item)
        else:
            print(RED + f"Incorrect. Correct answer: {item['answer']}" + RESET)
            local_missed.append(item)
            add_missed_question(progress, item)

        pause()

    percent = round((score / len(questions)) * 100) if questions else 0

    progress["total_quizzes"] += 1
    progress["best_score"] = max(progress["best_score"], percent)
    progress["quiz_history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "quiz_name": quiz_name,
        "score": score,
        "total": len(questions),
        "percent": percent
    })

    save_progress(progress)

    clear_screen()
    print_header("ROUND COMPLETE")
    print(GREEN + f"Score: {score}/{len(questions)}" + RESET)
    print(PINK + f"Percent: {percent}%" + RESET)

    if local_missed:
        print(RED + "\nMissed this round:" + RESET)
        for item in local_missed:
            print(f"- {item['question']}")
            print(f"  {DIM}Answer: {item['answer']}{RESET}")
    else:
        print(GREEN + "\nPerfect score. Great job." + RESET)

    pause()

def review_missed_questions(progress):
    missed = progress.get("missed_questions", [])
    if not missed:
        clear_screen()
        print_header("REVIEW MISSED QUESTIONS")
        print(GREEN + "You have no saved missed questions right now." + RESET)
        pause()
        return

    run_quiz(
        progress,
        "Missed Questions Review",
        missed,
        round_size=len(missed),
        timed=False
    )

def mixed_quiz(progress):
    combined = DOMAIN_1 + DOMAIN_2 + DOMAIN_3 + DOMAIN_4 + DOMAIN_5
    run_quiz(progress, "Mixed Quiz", combined, round_size=15, timed=False)

def timed_mixed_quiz(progress):
    combined = DOMAIN_1 + DOMAIN_2 + DOMAIN_3 + DOMAIN_4 + DOMAIN_5
    run_quiz(progress, "Timed Mixed Quiz", combined, round_size=10, timed=True, seconds=15)

def main():
    progress = load_progress()

    while True:
        show_banner()
        show_stats(progress)
        print()
        print_header("MAIN MENU")
        print(CYAN + "1. Domain 1 quiz - Security Concepts" + RESET)
        print(CYAN + "2. Domain 2 quiz - Threats and Vulnerabilities" + RESET)
        print(CYAN + "3. Domain 3 quiz - Architecture and Design" + RESET)
        print(CYAN + "4. Domain 4 quiz - Security Operations" + RESET)
        print(CYAN + "5. Domain 5 quiz - Governance and Risk" + RESET)
        print(CYAN + "6. Mixed quiz" + RESET)
        print(CYAN + "7. Timed mixed quiz" + RESET)
        print(CYAN + "8. Review missed questions" + RESET)
        print(CYAN + "9. Flashcards" + RESET)
        print(CYAN + "10. Memory sheet" + RESET)
        print(CYAN + "11. Quiz history" + RESET)
        print(CYAN + "12. Reset progress" + RESET)
        print(CYAN + "0. Exit" + RESET)

        choice = input("\nChoose an option: ").strip()

        if choice in QUIZ_GROUPS:
            quiz_name, bank = QUIZ_GROUPS[choice]
            run_quiz(progress, quiz_name, bank, round_size=min(8, len(bank)), timed=False)
        elif choice == "6":
            mixed_quiz(progress)
        elif choice == "7":
            timed_mixed_quiz(progress)
        elif choice == "8":
            review_missed_questions(progress)
        elif choice == "9":
            show_flashcards()
        elif choice == "10":
            show_memory_sheet()
        elif choice == "11":
            show_history(progress)
        elif choice == "12":
            confirm = input(RED + "Type RESET to erase progress: " + RESET).strip()
            if confirm == "RESET":
                progress = default_progress()
                save_progress(progress)
                print(GREEN + "Progress reset." + RESET)
                pause()
        elif choice == "0":
            clear_screen()
            print_header("GOOD LUCK")
            print(GREEN + "Keep going. Little by little every day until March 31." + RESET)
            break
        else:
            print(RED + "Invalid choice." + RESET)
            pause()

if __name__ == "__main__":
    main()
