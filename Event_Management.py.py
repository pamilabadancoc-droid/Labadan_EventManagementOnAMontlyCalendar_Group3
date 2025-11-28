import calendar
import datetime

# Global dictionary to store all events
# Format: {"YYYY-M": {"D": "Event Name", ...}, ...}
all_events = {
    # Initial data for demonstration purposes (e.g., Nov 2025)
    f"{datetime.date.today().year}-{datetime.date.today().month}": {
        "28": "Project Deadline",
        "30": "Team Meeting"
    }
}

# ---------- Display Calendar ----------
def show_calendar(year, month):
    """Prints a monthly calendar, marking today's date and event days with a '*'."""
    today = datetime.date.today()
    print(f"\n🗓️ {calendar.month_name[month]} {year}\nMo Tu We Th Fr Sa Su")
    
    # Get events for the current month, or an empty dict if none exist
    month_events = all_events.get(f"{year}-{month}", {})
    
    for week in calendar.monthcalendar(year, month):
        for day in week:
            if day == 0:
                print("   ", end=" ")
            else:
                # Format the day number
                s = f"{day:2}"
                
                # Check conditions
                is_today = (day == today.day and month == today.month and year == today.year)
                has_event = str(day) in month_events
                
                # Add '*' if it's today OR an event exists
                if is_today or has_event:
                    # To handle cases where today is also an event day, 
                    # we ensure the '*' is appended only once.
                    s += "*"
                
                print(f"{s:3}", end=" ")
        print()

# ---------- View Events ----------
def view_events(year=None, month=None):
    """Displays events for a specific month or all saved events."""
    # Specific month view
    if year and month:
        key = f"{year}-{month}"
        events = all_events.get(key, {})
        
        if not events:
            print("\nNo events for this month.")
            return

        print(f"\n📅 Events for {calendar.month_name[month]} {year}:")
        # Sort by day number
        for d, e in sorted(events.items(), key=lambda x: int(x[0])):
            print(f"  Day {d}: {e}")
        return

    # All events view
    if not all_events:
        print("\nNo events saved yet.")
        return

    print("\n--- All Saved Events ---")
    # Sort months by year and then month
    for k, ev in sorted(all_events.items()):
        y, m = map(int, k.split("-"))
        
        if not ev: # Skip months with no events (shouldn't happen with setdefault, but safe)
            continue
            
        print(f"\n🗓️ {calendar.month_name[m]} {y}:")
        # Sort events within the month by day number
        for d, e in sorted(ev.items(), key=lambda x: int(x[0])):
            print(f"  Day {d}: {e}")

# ---------- Add Event ----------
def add_event(year, month):
    """Prompts user for a day and event name to add to the calendar."""
    max_day = calendar.monthrange(year, month)[1]

    while True:
        day_input = input(f"Day (1-{max_day}) or 'c' to cancel: ")

        if day_input.lower() == "c":
            print("⚠️ Cancelled.")
            return

        try:
            day = int(day_input)
        except ValueError:
            print("❌ Invalid number. Try again.")
            continue

        if not (1 <= day <= max_day):
            print(f"❌ Day must be 1–{max_day}.")
            continue

        # Check if the date is in the past
        try:
            target_date = datetime.date(year, month, day)
            if target_date < datetime.date.today():
                print("❌ Cannot select a past day.")
                continue
        except ValueError:
            # This handles cases where day, month, or year combination is invalid (e.g., Feb 30)
            # which is largely prevented by max_day check, but is a safe guard.
            print("❌ Invalid date. Try again.")
            continue

        break

    event_name = input("Event: ").strip()
    if not event_name:
        print("❌ Event name cannot be empty. Cancelled.")
        return
        
    # Use str(day) for dictionary key consistency
    all_events.setdefault(f"{year}-{month}", {})[str(day)] = event_name
    print(f"✅ Event added on {calendar.month_name[month]} {day}, {year}.")

# ---------- Delete Event ----------
def delete_event(year, month):
    """Prompts user for a day to delete an event from the calendar."""
    key = f"{year}-{month}"
    month_events = all_events.get(key)

    if not month_events:
        print("⚠️ No events to delete in this month.")
        return

    # Show existing events to the user before asking which one to delete
    print("\nExisting events in this month:")
    for d, e in sorted(month_events.items(), key=lambda x: int(x[0])):
        print(f"  Day {d}: {e}")

    while True:
        day_input = input("Day to delete or 'c' to cancel: ")

        if day_input.lower() == "c":
            print("⚠️ Cancelled.")
            return

        # Check if the input day (as a string) has an event
        if day_input in month_events:
            # We assume day_input is the string key used in all_events
            del month_events[day_input]
            
            # Clean up empty month entry to keep all_events tidy
            if not month_events:
                del all_events[key]
                
            print(f"🗑️ Event on day {day_input} deleted.")
            return
        else:
            print("❌ No event on that day. Try again.")

# ---------- Get Year & Month ----------
def get_year_month():
    """Prompts user for a future or current year and month."""
    today = datetime.date.today()

    # Year
    while True:
        y_input = input("Year (e.g., 2025) or 'c' to cancel: ")

        if y_input.lower() == "c":
            return None, None

        try:
            y = int(y_input)
        except ValueError:
            print("❌ Invalid year. Try again.")
            continue

        if y < today.year:
            print("❌ Cannot select past year.")
            continue

        break

    # Month
    while True:
        m_input = input("Month (1-12) or 'c' to cancel: ")

        if m_input.lower() == "c":
            return None, None

        try:
            m = int(m_input)
        except ValueError:
            print("❌ Invalid month. Try again.")
            continue

        if not 1 <= m <= 12:
            print("❌ Month must be 1–12.")
            continue

        # Check if the month is in the past for the current year
        if y == today.year and m < today.month:
            print("❌ Cannot select past month.")
            continue

        break

    return y, m

# ---------- Exit ----------
def exit_menu():
    """Confirms user's intent to exit the program."""
    choice = input("\n1. Confirm Exit\n2. Cancel\nChoose: ").strip()
    return choice == "1"

# ---------- Main Loop ----------
def main():
    """The main function to run the calendar application."""
    while True:
        print("\n--- 📆 CALENDAR MENU ---")
        print("1. View Calendar (Select Month)")
        print("2. Add Event (Select Month)")
        print("3. Delete Event (Select Month)")
        print("4. View Events for This Month")
        print("5. View All Events")
        print("6. Exit")

        choice = input("Choose option (1-6): ").strip()

        if choice in ["1", "2", "3"]:
            y, m = get_year_month()
            if not y:
                print("⚠️ Action cancelled.") # Changed from 'Cancelled.' for clarity
                continue

            if choice == "1":
                show_calendar(y, m)
            elif choice == "2":
                add_event(y, m)
            elif choice == "3":
                delete_event(y, m)

        elif choice == "4":
            today = datetime.date.today()
            view_events(today.year, today.month)

        elif choice == "5":
            view_events()

        elif choice == "6":
            if exit_menu():
                print("👋 Goodbye!")
                break

        else:
            print("❌ Invalid choice. Please select 1-6.") # Added helpful message

# FIXED main block to allow execution
if __name__ == "__main__":
    main()