#!/usr/bin/env python3
"""
Gesture GUI Components
Handles the graphical user interface for gesture management
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, Callable


class GestureSettingsGUI:
    """Main settings GUI for gesture management"""
    
    def __init__(self, profile_manager, gesture_recorder, recording_session):
        self.profile_manager = profile_manager
        self.gesture_recorder = gesture_recorder
        self.recording_session = recording_session
        
        self.root = None
        self.settings_window = None
        self.settings_open = False
        
        # UI Components
        self.profile_listbox = None
        self.gesture_tree = None
        self.current_profile_label = None
        self.selected_profile_label = None
        self.manage_profile_label = None
        self.gesture_name_entry = None
        self.key_binding_entry = None
        self.hand_type_var = None
        self.recording_status_label = None
        self.record_button = None
        
        # Set up recorder callbacks
        self.gesture_recorder.set_status_callback(self.update_recording_status)
    
    def initialize_root(self):
        """Initialize tkinter root if not exists"""
        if not self.root:
            self.root = tk.Tk()
            self.root.withdraw()  # Hide main window
    
    def open_settings_window(self):
        """Open the enhanced settings configuration window"""
        if self.settings_open:
            if self.settings_window:
                try:
                    self.settings_window.lift()
                except:
                    pass
            return

        try:
            self.settings_open = True
            self.initialize_root()

            self.settings_window = tk.Toplevel(self.root)
            self.settings_window.title("🎮 Enhanced Gesture Settings")
            self.settings_window.geometry("900x700")
            self.settings_window.protocol("WM_DELETE_WINDOW", self.close_settings_window)
            self.root.update()
        except Exception as e:
            print(f"❌ Error opening settings window: {e}")
            self.settings_open = False
            return

        # Create main container
        main_frame = ttk.Frame(self.settings_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create the simplified interface
        self.create_simplified_interface(main_frame)

    def create_simplified_interface(self, parent):
        """Create simplified, user-friendly interface"""
        # Title
        title_label = ttk.Label(parent, text="🎮 Gesture Profile Manager",
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))

        # Step 1: Profile Selection/Creation
        profile_section = ttk.LabelFrame(parent, text="Step 1: Select or Create Profile", padding=15)
        profile_section.pack(fill='x', pady=(0, 15))

        # Current profile display
        current_frame = ttk.Frame(profile_section)
        current_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(current_frame, text="Current Profile:",
                 font=('Arial', 12, 'bold')).pack(side='left')

        current_profile_name = self.profile_manager.current_profile or "None Selected"
        self.current_profile_label = ttk.Label(current_frame, text=current_profile_name,
                                              font=('Arial', 12), foreground='blue')
        self.current_profile_label.pack(side='left', padx=(10, 0))

        # Profile selection and creation
        profile_controls = ttk.Frame(profile_section)
        profile_controls.pack(fill='x')

        # Profile dropdown
        ttk.Label(profile_controls, text="Select Profile:").pack(side='left')
        self.profile_var = tk.StringVar()
        self.profile_dropdown = ttk.Combobox(profile_controls, textvariable=self.profile_var,
                                           state='readonly', width=20)
        self.profile_dropdown.pack(side='left', padx=(5, 10))
        self.profile_dropdown.bind('<<ComboboxSelected>>', self.on_profile_selected)

        # Profile buttons
        ttk.Button(profile_controls, text="📂 New Profile",
                  command=self.create_new_profile_simple).pack(side='left', padx=2)

        ttk.Button(profile_controls, text="🏎️ Racing",
                  command=lambda: self.create_template_profile_simple("Racing Game")).pack(side='left', padx=2)

        ttk.Button(profile_controls, text="🎥 Video",
                  command=lambda: self.create_template_profile_simple("Video Player")).pack(side='left', padx=2)

        ttk.Button(profile_controls, text="🎮 Gaming",
                  command=lambda: self.create_template_profile_simple("General Gaming")).pack(side='left', padx=2)

        # Step 2: Add Gestures
        gesture_section = ttk.LabelFrame(parent, text="Step 2: Add Gestures to Profile", padding=15)
        gesture_section.pack(fill='both', expand=True, pady=(0, 15))

        # Instructions
        instructions = ttk.Label(gesture_section,
                               text="Add gestures one by one. Each gesture will be recorded with a 3-2-1 countdown.\n"
                                    "• Single: Use one hand only\n"
                                    "• Both: Use both hands together (great for numbers 6-10)\n"
                                    "• Multiple gestures can use the same key binding",
                               font=('Arial', 10), foreground='darkblue')
        instructions.pack(pady=(0, 10))

        # Key binding help
        key_help = ttk.Label(gesture_section,
                           text="Key Examples: 'a', 'space', 'enter', 'shift', 'ctrl+c', 'alt+tab', 'f1', 'up', 'down'",
                           font=('Arial', 9), foreground='gray')
        key_help.pack(pady=(0, 5))

        # Add gesture form
        add_frame = ttk.Frame(gesture_section)
        add_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(add_frame, text="Gesture Name:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.gesture_name_entry = ttk.Entry(add_frame, width=15)
        self.gesture_name_entry.grid(row=0, column=1, padx=(0, 10))

        ttk.Label(add_frame, text="Key:").grid(row=0, column=2, sticky='w', padx=(0, 5))
        self.key_binding_entry = ttk.Entry(add_frame, width=10)
        self.key_binding_entry.grid(row=0, column=3, padx=(0, 10))

        # Hand type selection
        ttk.Label(add_frame, text="Type:").grid(row=0, column=4, sticky='w', padx=(0, 5))
        self.hand_type_var = tk.StringVar(value="single")
        hand_combo = ttk.Combobox(add_frame, textvariable=self.hand_type_var,
                                 values=["single", "both"], state="readonly", width=8)
        hand_combo.grid(row=0, column=5, padx=(0, 10))

        self.record_button = ttk.Button(add_frame, text="🔴 Record Gesture",
                                       command=self.record_gesture_simple)
        self.record_button.grid(row=0, column=6, padx=(0, 10))

        # Recording status
        self.recording_status_label = ttk.Label(gesture_section,
                                               text="Ready to record gesture",
                                               font=('Arial', 11))
        self.recording_status_label.pack(pady=5)

        # Gesture list
        list_frame = ttk.Frame(gesture_section)
        list_frame.pack(fill='both', expand=True, pady=(10, 0))

        ttk.Label(list_frame, text="Gestures in Profile:", font=('Arial', 12, 'bold')).pack(anchor='w')

        # Create treeview for gestures
        columns = ('Name', 'Key', 'Type')
        self.gesture_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)

        self.gesture_tree.heading('Name', text='Gesture Name')
        self.gesture_tree.heading('Key', text='Key Binding')
        self.gesture_tree.heading('Type', text='Hand Type')

        self.gesture_tree.column('Name', width=150)
        self.gesture_tree.column('Key', width=100)
        self.gesture_tree.column('Type', width=100)

        # Scrollbar for treeview
        tree_scrollbar = ttk.Scrollbar(list_frame, orient='vertical',
                                      command=self.gesture_tree.yview)
        self.gesture_tree.configure(yscrollcommand=tree_scrollbar.set)

        tree_container = ttk.Frame(list_frame)
        tree_container.pack(fill='both', expand=True)

        self.gesture_tree.pack(side='left', fill='both', expand=True)
        tree_scrollbar.pack(side='right', fill='y')

        # Gesture management buttons
        gesture_buttons = ttk.Frame(gesture_section)
        gesture_buttons.pack(fill='x', pady=(10, 0))

        ttk.Button(gesture_buttons, text="🗑️ Delete Gesture",
                  command=self.delete_selected_gesture).pack(side='left', padx=5)

        ttk.Button(gesture_buttons, text="💾 Save Profile",
                  command=self.save_current_profile).pack(side='left', padx=5)

        ttk.Button(gesture_buttons, text="🎮 Activate Profile",
                  command=self.activate_current_profile).pack(side='left', padx=5)

        # Step 3: Profile Status
        status_section = ttk.LabelFrame(parent, text="Step 3: Profile Status", padding=15)
        status_section.pack(fill='x')

        self.status_label = ttk.Label(status_section,
                                     text="Select a profile to get started",
                                     font=('Arial', 11))
        self.status_label.pack()

        # Initialize
        self.refresh_profile_dropdown()
        self.refresh_gesture_list()
        self.update_status()

    def refresh_profile_dropdown(self):
        """Refresh the profile dropdown list"""
        if hasattr(self, 'profile_dropdown'):
            profiles = self.profile_manager.get_profile_names()
            self.profile_dropdown['values'] = profiles

            # Set current selection
            if self.profile_manager.current_profile in profiles:
                self.profile_var.set(self.profile_manager.current_profile)
            elif profiles:
                self.profile_var.set('')

    def on_profile_selected(self, event=None):
        """Handle profile selection from dropdown"""
        selected_profile = self.profile_var.get()
        if selected_profile and selected_profile != self.profile_manager.current_profile:
            if self.profile_manager.load_profile(selected_profile):
                self.update_profile_labels()
                self.refresh_gesture_list()
                self.update_status()
                print(f"✅ Loaded profile: {selected_profile}")

    def create_new_profile_simple(self):
        """Simple profile creation dialog"""
        name = tk.simpledialog.askstring("New Profile", "Enter profile name:")
        if name and name.strip():
            name = name.strip()
            if name in self.profile_manager.get_profile_names():
                messagebox.showerror("Error", "Profile name already exists")
                return

            if self.profile_manager.create_profile(name, f"Custom profile: {name}"):
                self.profile_manager.load_profile(name)
                self.refresh_profile_dropdown()
                self.update_profile_labels()
                self.refresh_gesture_list()
                self.update_status()
                messagebox.showinfo("Success", f"Profile '{name}' created and loaded!")
            else:
                messagebox.showerror("Error", "Failed to create profile")

    def create_template_profile_simple(self, template_name):
        """Create and load a template profile"""
        if template_name in self.profile_manager.get_profile_names():
            # Ask if user wants to load existing or replace
            result = messagebox.askyesnocancel("Profile Exists",
                                             f"Profile '{template_name}' already exists.\n\n"
                                             f"Yes: Load existing profile\n"
                                             f"No: Replace with new template\n"
                                             f"Cancel: Do nothing")
            if result is None:  # Cancel
                return
            elif result:  # Yes - load existing
                self.profile_manager.load_profile(template_name)
                self.refresh_profile_dropdown()
                self.update_profile_labels()
                self.refresh_gesture_list()
                self.update_status()
                return
            else:  # No - replace
                self.profile_manager.delete_profile(template_name)

        # Create new template
        if self.profile_manager.create_template_profile(template_name):
            self.profile_manager.load_profile(template_name)
            self.refresh_profile_dropdown()
            self.update_profile_labels()
            self.refresh_gesture_list()
            self.update_status()
            messagebox.showinfo("Success", f"Template '{template_name}' created!\n\n"
                                         f"Now you can add gestures one by one.")
        else:
            messagebox.showerror("Error", "Failed to create template profile")

    def record_gesture_simple(self):
        """Simple gesture recording - immediate recording with countdown"""
        if not self.profile_manager.current_profile:
            messagebox.showerror("Error", "Please select or create a profile first")
            return

        gesture_name = self.gesture_name_entry.get().strip()
        key_binding = self.key_binding_entry.get().strip()

        if not gesture_name:
            messagebox.showerror("Error", "Please enter a gesture name")
            self.gesture_name_entry.focus()
            return

        if not key_binding:
            messagebox.showerror("Error", "Please enter a key binding")
            self.key_binding_entry.focus()
            return

        # Check if gesture already exists
        profile_data = self.profile_manager.get_current_profile_data()
        if profile_data and gesture_name in profile_data.get('gestures', {}):
            result = messagebox.askyesno("Gesture Exists",
                                       f"Gesture '{gesture_name}' already exists. Replace it?")
            if not result:
                return

        # Check if key binding is already used by another gesture
        if profile_data:
            existing_bindings = profile_data.get('bindings', {})
            conflicting_gestures = [g_name for g_name, g_key in existing_bindings.items()
                                  if g_key == key_binding and g_name != gesture_name]

            if conflicting_gestures:
                conflict_list = ', '.join(conflicting_gestures)
                result = messagebox.askyesnocancel(
                    "Key Binding Conflict",
                    f"Key '{key_binding}' is already bound to: {conflict_list}\n\n"
                    f"Do you want to bind '{gesture_name}' to the same key?\n\n"
                    f"Yes: Add another gesture with same key\n"
                    f"No: Choose a different key\n"
                    f"Cancel: Stop recording"
                )

                if result is None:  # Cancel
                    return
                elif result is False:  # No - choose different key
                    messagebox.showinfo("Choose Different Key",
                                      f"Please enter a different key binding for '{gesture_name}'")
                    self.key_binding_entry.focus()
                    return
                # If Yes, continue with the recording

        # Get hand type
        hand_type = self.hand_type_var.get()

        # Show appropriate message for both-hand recording
        if hand_type == "both":
            messagebox.showinfo("Both-Hand Recording",
                               "You selected both-hand recording.\n\n"
                               "During recording:\n"
                               "• Show your gesture using BOTH hands\n"
                               "• For numbers 6-10: Use both hands together\n"
                               "• Example: 6 = 5 fingers (right) + 1 finger (left)")

        # Disable the record button and show status
        self.record_button.config(state='disabled', text="🔴 Recording...")

        # Start recording session if not active
        if not self.recording_session.current_profile:
            self.recording_session.start_session(self.profile_manager.current_profile)

        # Start recording immediately
        self.recording_session.record_gesture(gesture_name, key_binding, hand_type)

        # Clear the form
        self.gesture_name_entry.delete(0, tk.END)
        self.key_binding_entry.delete(0, tk.END)

        # Set up completion callback
        def on_recording_complete():
            try:
                self.record_button.config(state='normal', text="🔴 Record Gesture")
                self.refresh_gesture_list()
                self.update_status()
                self.gesture_name_entry.focus()  # Focus back to name entry for next gesture
            except Exception as e:
                print(f"Warning: Error in completion callback: {e}")

        # Schedule GUI reset after recording completes
        if self.settings_window:
            self.settings_window.after(7000, on_recording_complete)  # 3s countdown + 3s recording + 1s buffer

    def update_status(self):
        """Update the status display safely"""
        if not hasattr(self, 'status_label') or not self.status_label:
            return

        try:
            # Check if the widget still exists
            self.status_label.winfo_exists()
        except tk.TclError:
            # Widget has been destroyed
            return

        if not self.profile_manager.current_profile:
            try:
                self.status_label.config(text="❌ No profile selected - Create or select a profile to get started")
            except tk.TclError:
                pass
            return

        profile_data = self.profile_manager.get_current_profile_data()
        if not profile_data:
            try:
                self.status_label.config(text="❌ Profile data not available")
            except tk.TclError:
                pass
            return

        total_gestures = len(profile_data.get('gestures', {}))

        try:
            if total_gestures == 0:
                self.status_label.config(text=f"✅ Profile '{self.profile_manager.current_profile}' loaded - Add gestures to get started")
            else:
                self.status_label.config(text=f"✅ Profile '{self.profile_manager.current_profile}' - {total_gestures} gestures ready")
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass

    def save_current_profile(self):
        """Save the current profile"""
        if not self.profile_manager.current_profile:
            messagebox.showerror("Error", "No profile selected")
            return

        profile_data = self.profile_manager.get_current_profile_data()
        if profile_data:
            # Activate all gestures in the profile
            gestures = profile_data.get('gestures', {})
            profile_data['active_gestures'] = list(gestures.keys())

            if self.profile_manager.save_profile(self.profile_manager.current_profile, profile_data):
                messagebox.showinfo("Success", f"Profile '{self.profile_manager.current_profile}' saved!\n\n"
                                              f"All {len(gestures)} gestures are ready to use.")
                self.update_status()
            else:
                messagebox.showerror("Error", "Failed to save profile")

    def activate_current_profile(self):
        """Activate the current profile for gesture recognition"""
        if not self.profile_manager.current_profile:
            messagebox.showerror("Error", "No profile selected")
            return

        profile_data = self.profile_manager.get_current_profile_data()
        if not profile_data:
            messagebox.showerror("Error", "Profile data not available")
            return

        gestures = profile_data.get('gestures', {})
        if not gestures:
            messagebox.showwarning("Warning", "Profile has no gestures to activate")
            return

        # Activate all gestures
        profile_data['active_gestures'] = list(gestures.keys())
        self.profile_manager.save_profile(self.profile_manager.current_profile, profile_data)

        messagebox.showinfo("Profile Activated",
                           f"Profile '{self.profile_manager.current_profile}' is now active!\n\n"
                           f"All {len(gestures)} gestures are ready to use.\n"
                           f"Press 'p' in the camera window to see profile selector.")

        # Update status before closing window
        self.update_status()

        # Close settings window
        self.close_settings_window()

    def open_profile_selector(self):
        """Open simplified profile selector window (triggered by 'p' key)"""
        # Create profile selector window
        selector_window = tk.Toplevel(self.root if self.root else None)
        selector_window.title("🎮 Profile Selector")
        selector_window.geometry("500x400")

        # Center the window
        selector_window.update_idletasks()
        x = (selector_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (selector_window.winfo_screenheight() // 2) - (400 // 2)
        selector_window.geometry(f"500x400+{x}+{y}")

        # Title
        title_label = ttk.Label(selector_window, text="🎮 Profile Selector",
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=15)

        # Current profile display
        current_frame = ttk.Frame(selector_window)
        current_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(current_frame, text="Currently Active:",
                 font=('Arial', 12, 'bold')).pack(side='left')

        current_name = self.profile_manager.current_profile or "None"
        current_label = ttk.Label(current_frame, text=current_name,
                                 font=('Arial', 12), foreground='green')
        current_label.pack(side='left', padx=(10, 0))

        # Profile list frame
        list_frame = ttk.LabelFrame(selector_window, text="Available Profiles", padding=15)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Create simple profile list
        self.create_simple_profile_list(list_frame, selector_window)

        # Bottom buttons
        button_frame = ttk.Frame(selector_window)
        button_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(button_frame, text="⚙️ Open Settings",
                  command=lambda: self.open_settings_from_selector(selector_window)).pack(side='left', padx=5)

        ttk.Button(button_frame, text="❌ Close",
                  command=selector_window.destroy).pack(side='right', padx=5)

        # Focus the window
        selector_window.focus_set()
        selector_window.grab_set()

    def create_simple_profile_list(self, parent, selector_window):
        """Create simple profile list with Load/Delete buttons"""
        # Get profiles quickly
        profiles = self.profile_manager.get_profile_names()

        if not profiles:
            ttk.Label(parent, text="No profiles available.\nCreate one in Settings.",
                     font=('Arial', 12), foreground='gray').pack(pady=20)
            return

        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add profiles
        for profile_name in profiles:
            self.create_simple_profile_row(scrollable_frame, profile_name, selector_window)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_simple_profile_row(self, parent, profile_name, selector_window):
        """Create a simple row for each profile"""
        # Create row frame
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill='x', pady=5, padx=5)

        # Profile info frame
        info_frame = ttk.Frame(row_frame)
        info_frame.pack(side='left', fill='x', expand=True)

        # Profile name
        name_label = ttk.Label(info_frame, text=f"📁 {profile_name}",
                              font=('Arial', 12, 'bold'))
        name_label.pack(anchor='w')

        # Quick gesture count using basic info
        try:
            basic_info = self.profile_manager.get_profile_basic_info(profile_name)
            if basic_info:
                gesture_count = basic_info.get('gesture_count', 0)
                count_text = f"{gesture_count} gestures"

                # Add description if available
                description = basic_info.get('description', '')
                if description and len(description) > 0:
                    # Truncate long descriptions
                    if len(description) > 30:
                        description = description[:30] + "..."
                    count_text += f" • {description}"
            else:
                count_text = "No info available"
        except:
            count_text = "Loading..."

        count_label = ttk.Label(info_frame, text=count_text,
                               font=('Arial', 10), foreground='gray')
        count_label.pack(anchor='w')

        # Current profile indicator
        if profile_name == self.profile_manager.current_profile:
            status_label = ttk.Label(info_frame, text="✅ Currently Active",
                                   font=('Arial', 10), foreground='green')
            status_label.pack(anchor='w')

        # Buttons frame
        button_frame = ttk.Frame(row_frame)
        button_frame.pack(side='right', padx=(10, 0))

        # Load button
        load_button = ttk.Button(button_frame, text="📂 Load",
                                command=lambda: self.load_profile_quick(profile_name, selector_window))
        load_button.pack(side='top', pady=2)

        # Delete button
        delete_button = ttk.Button(button_frame, text="🗑️ Delete",
                                  command=lambda: self.delete_profile_quick(profile_name, selector_window))
        delete_button.pack(side='top', pady=2)

        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=5)

    def load_profile_quick(self, profile_name, selector_window):
        """Quickly load and activate a profile"""
        try:
            # Load profile
            if self.profile_manager.load_profile(profile_name):
                # Activate all gestures in the profile
                profile_data = self.profile_manager.get_current_profile_data()
                if profile_data:
                    gestures = profile_data.get('gestures', {})
                    profile_data['active_gestures'] = list(gestures.keys())
                    self.profile_manager.save_profile(profile_name, profile_data)

                    # Show success message
                    messagebox.showinfo("Profile Loaded",
                                       f"✅ Profile '{profile_name}' loaded and activated!\n\n"
                                       f"🎮 {len(gestures)} gestures ready to use.")

                    # Close selector window
                    selector_window.destroy()

                    # Update any open settings window
                    self.update_profile_labels()
                else:
                    messagebox.showerror("Error", "Failed to load profile data")
            else:
                messagebox.showerror("Error", "Failed to load profile")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load profile: {e}")

    def delete_profile_quick(self, profile_name, selector_window):
        """Quickly delete a profile with confirmation"""
        result = messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete profile '{profile_name}'?\n\n"
                                   f"This action cannot be undone.")
        if result:
            try:
                if self.profile_manager.delete_profile(profile_name):
                    messagebox.showinfo("Success", f"Profile '{profile_name}' deleted successfully!")

                    # Refresh the profile list
                    selector_window.destroy()
                    self.open_profile_selector()  # Reopen with updated list

                    # Update any open settings window
                    self.update_profile_labels()
                else:
                    messagebox.showerror("Error", "Failed to delete profile")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete profile: {e}")

    # Old complex profile list methods removed - using simplified version

    def open_settings_from_selector(self, selector_window):
        """Open settings window from profile selector"""
        selector_window.destroy()
        self.open_settings_window()
    
    def create_profile_management_tab_OLD(self, parent):
        """Create profile management tab"""
        # Title
        title_label = ttk.Label(parent, text="📁 Gesture Profile Management", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Current profile display
        current_frame = ttk.Frame(parent)
        current_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(current_frame, text="Current Profile:", 
                 font=('Arial', 12, 'bold')).pack(side='left')
        
        current_profile_name = self.profile_manager.current_profile or "None"
        self.current_profile_label = ttk.Label(current_frame, text=current_profile_name,
                                              font=('Arial', 12), foreground='blue')
        self.current_profile_label.pack(side='left', padx=(10, 0))

        # Profile list
        list_frame = ttk.LabelFrame(parent, text="Available Profiles", padding=10)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Profile listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill='both', expand=True)

        self.profile_listbox = tk.Listbox(listbox_frame, height=8)
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', 
                                 command=self.profile_listbox.yview)
        self.profile_listbox.configure(yscrollcommand=scrollbar.set)

        self.profile_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="📂 Create New Profile",
                  command=self.create_new_profile_dialog).pack(side='left', padx=5)

        ttk.Button(button_frame, text="📋 Load Profile",
                  command=self.load_selected_profile).pack(side='left', padx=5)

        ttk.Button(button_frame, text="🔄 Refresh List",
                  command=self.refresh_profile_list).pack(side='left', padx=5)

        ttk.Button(button_frame, text="🗑️ Delete Profile",
                  command=self.delete_selected_profile).pack(side='left', padx=5)

        # Profile templates
        template_frame = ttk.LabelFrame(parent, text="Quick Templates", padding=10)
        template_frame.pack(fill='x', padx=20, pady=10)

        template_buttons = ttk.Frame(template_frame)
        template_buttons.pack()

        ttk.Button(template_buttons, text="🏎️ Racing Game",
                  command=lambda: self.create_template_profile("Racing Game")).pack(side='left', padx=5)

        ttk.Button(template_buttons, text="🎥 Video Player",
                  command=lambda: self.create_template_profile("Video Player")).pack(side='left', padx=5)

        ttk.Button(template_buttons, text="🎮 General Gaming",
                  command=lambda: self.create_template_profile("General Gaming")).pack(side='left', padx=5)

        # Initial refresh
        self.refresh_profile_list()
    
    def create_add_gesture_tab_OLD(self, parent):
        """Create add gesture tab"""
        # Title
        title_label = ttk.Label(parent, text="➕ Add Gesture to Profile", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Profile selection
        profile_frame = ttk.Frame(parent)
        profile_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(profile_frame, text="Profile:", font=('Arial', 12, 'bold')).pack(side='left')
        
        self.selected_profile_label = ttk.Label(profile_frame, 
                                               text=self.profile_manager.current_profile or "No profile selected",
                                               font=('Arial', 12), foreground='blue')
        self.selected_profile_label.pack(side='left', padx=(10, 0))

        # Template gestures section
        template_frame = ttk.LabelFrame(parent, text="Template Gestures", padding=10)
        template_frame.pack(fill='x', padx=20, pady=10)

        # Template gestures list
        self.create_template_gestures_section(template_frame)

        # Custom gesture details
        details_frame = ttk.LabelFrame(parent, text="Custom Gesture Details", padding=10)
        details_frame.pack(fill='x', padx=20, pady=10)

        # Gesture name
        name_frame = ttk.Frame(details_frame)
        name_frame.pack(fill='x', pady=5)
        ttk.Label(name_frame, text="Gesture Name:", width=15).pack(side='left')
        self.gesture_name_entry = ttk.Entry(name_frame, width=20)
        self.gesture_name_entry.pack(side='left', padx=(5, 0))

        # Key binding
        key_frame = ttk.Frame(details_frame)
        key_frame.pack(fill='x', pady=5)
        ttk.Label(key_frame, text="Key Binding:", width=15).pack(side='left')
        self.key_binding_entry = ttk.Entry(key_frame, width=20)
        self.key_binding_entry.pack(side='left', padx=(5, 0))

        # Help text for key bindings
        help_text = ttk.Label(details_frame, 
                             text="Examples: 'a', 'space', 'enter', 'up', 'down', 'left', 'right', 'ctrl+c'",
                             font=('Arial', 9), foreground='gray')
        help_text.pack(pady=2)

        # Hand type selection
        hand_frame = ttk.Frame(details_frame)
        hand_frame.pack(fill='x', pady=5)
        ttk.Label(hand_frame, text="Hand Type:", width=15).pack(side='left')
        self.hand_type_var = tk.StringVar(value="single")
        hand_radio_frame = ttk.Frame(hand_frame)
        hand_radio_frame.pack(side='left', padx=(5, 0))
        ttk.Radiobutton(hand_radio_frame, text="Single Hand", 
                       variable=self.hand_type_var, value="single").pack(side='left')
        ttk.Radiobutton(hand_radio_frame, text="Both Hands", 
                       variable=self.hand_type_var, value="both").pack(side='left', padx=(10, 0))

        # Recording section
        recording_frame = ttk.LabelFrame(parent, text="Record Gesture", padding=10)
        recording_frame.pack(fill='x', padx=20, pady=10)

        # Recording status
        self.recording_status_label = ttk.Label(recording_frame, 
                                               text="Ready to record gesture",
                                               font=('Arial', 12))
        self.recording_status_label.pack(pady=5)

        # Recording button
        self.record_button = ttk.Button(recording_frame, text="🔴 Start Recording",
                                       command=self.start_gesture_recording_gui)
        self.record_button.pack(pady=5)

        # Instructions
        instructions = ttk.Label(recording_frame,
                               text="1. Enter gesture name and key binding\n2. Click 'Start Recording'\n3. Wait for countdown (3, 2, 1)\n4. Hold your gesture steady for 3 seconds",
                               font=('Arial', 10), foreground='darkblue')
        instructions.pack(pady=10)
    
    def create_template_gestures_section(self, parent):
        """Create template gestures section"""
        info_label = ttk.Label(parent, 
                              text="Quick setup: Select a template gesture and record it",
                              font=('Arial', 10), foreground='darkblue')
        info_label.pack(pady=5)
        
        # Template gestures frame
        template_gestures_frame = ttk.Frame(parent)
        template_gestures_frame.pack(fill='both', expand=True, pady=5)
        
        # This will be populated when a profile is loaded
        self.template_gestures_frame = template_gestures_frame
        self.refresh_template_gestures()
    
    def refresh_template_gestures(self):
        """Refresh template gestures display"""
        # Clear existing widgets
        for widget in self.template_gestures_frame.winfo_children():
            widget.destroy()
        
        if not self.profile_manager.current_profile:
            ttk.Label(self.template_gestures_frame, 
                     text="Load a profile to see template gestures",
                     font=('Arial', 10), foreground='gray').pack()
            return
        
        template_gestures = self.profile_manager.get_template_gestures(self.profile_manager.current_profile)
        
        if not template_gestures:
            ttk.Label(self.template_gestures_frame, 
                     text="No template gestures available for this profile",
                     font=('Arial', 10), foreground='gray').pack()
            return
        
        # Create buttons for each template gesture
        for gesture_name, gesture_info in template_gestures.items():
            gesture_frame = ttk.Frame(self.template_gestures_frame)
            gesture_frame.pack(fill='x', pady=2)
            
            # Gesture info
            info_text = f"{gesture_name}: {gesture_info['key']} - {gesture_info['description']}"
            ttk.Label(gesture_frame, text=info_text, width=50).pack(side='left')
            
            # Record button
            ttk.Button(gesture_frame, text="🔴 Record",
                      command=lambda gn=gesture_name, gi=gesture_info: self.record_template_gesture(gn, gi)).pack(side='right')
    
    def record_template_gesture(self, gesture_name: str, gesture_info: dict):
        """Record a template gesture"""
        if not self.profile_manager.current_profile:
            messagebox.showerror("Error", "Please load a profile first")
            return
        
        # Fill in the form with template data
        self.gesture_name_entry.delete(0, tk.END)
        self.gesture_name_entry.insert(0, gesture_name)
        
        self.key_binding_entry.delete(0, tk.END)
        self.key_binding_entry.insert(0, gesture_info['key'])
        
        # Start recording
        self.start_gesture_recording_gui()
    
    def update_recording_status(self, message: str, color: str = 'black'):
        """Update recording status in GUI (thread-safe)"""
        if hasattr(self, 'recording_status_label') and self.recording_status_label:
            # Use after_idle to ensure GUI updates happen in main thread
            if hasattr(self, 'root') and self.root:
                self.root.after_idle(lambda: self._update_status_label(message, color))
            elif hasattr(self, 'settings_window') and self.settings_window:
                self.settings_window.after_idle(lambda: self._update_status_label(message, color))

    def _update_status_label(self, message: str, color: str):
        """Internal method to update status label (called from main thread)"""
        if hasattr(self, 'recording_status_label') and self.recording_status_label:
            try:
                # Check if widget still exists
                self.recording_status_label.winfo_exists()
                self.recording_status_label.config(text=message, foreground=color)
            except tk.TclError:
                # Widget has been destroyed, ignore
                pass
            except Exception as e:
                print(f"Warning: Could not update status label: {e}")
    
    def reset_recording_gui(self):
        """Reset recording GUI elements (thread-safe)"""
        if hasattr(self, 'root') and self.root:
            self.root.after_idle(self._reset_gui_elements)
        elif hasattr(self, 'settings_window') and self.settings_window:
            self.settings_window.after_idle(self._reset_gui_elements)

    def _reset_gui_elements(self):
        """Internal method to reset GUI elements (called from main thread)"""
        try:
            if hasattr(self, 'record_button') and self.record_button:
                self.record_button.winfo_exists()
                self.record_button.config(state='normal', text="🔴 Record Gesture")
        except tk.TclError:
            pass
        except Exception as e:
            print(f"Warning: Could not reset record button: {e}")

        try:
            if hasattr(self, 'recording_status_label') and self.recording_status_label:
                self.recording_status_label.winfo_exists()
                self.recording_status_label.config(text="Ready to record gesture", foreground='black')
        except tk.TclError:
            pass
        except Exception as e:
            print(f"Warning: Could not reset status label: {e}")
    
    def start_gesture_recording_gui(self):
        """Start gesture recording from GUI"""
        if not self.profile_manager.current_profile:
            messagebox.showerror("Error", "Please load a profile first")
            return

        gesture_name = self.gesture_name_entry.get().strip()
        key_binding = self.key_binding_entry.get().strip()

        if not gesture_name:
            messagebox.showerror("Error", "Please enter a gesture name")
            return

        if not key_binding:
            messagebox.showerror("Error", "Please enter a key binding")
            return

        # Check if gesture already exists
        profile_data = self.profile_manager.get_current_profile_data()
        if profile_data and gesture_name in profile_data.get('gestures', {}):
            result = messagebox.askyesno("Gesture Exists", 
                                       f"Gesture '{gesture_name}' already exists. Replace it?")
            if not result:
                return

        hand_type = self.hand_type_var.get()
        
        # Update UI
        self.record_button.config(state='disabled', text="🔴 Recording...")
        
        # Start recording session if not active
        if not self.recording_session.current_profile:
            self.recording_session.start_session(self.profile_manager.current_profile)
        
        # Start recording
        self.recording_session.record_gesture(gesture_name, key_binding, hand_type)
        
        # Set up completion callback to reset GUI
        def on_completion():
            try:
                self.reset_recording_gui()
                self.refresh_gesture_list()
                self.refresh_template_gestures()
            except Exception as e:
                print(f"Warning: Error in completion callback: {e}")

        # Schedule GUI reset after recording completes (thread-safe)
        if self.settings_window:
            self.settings_window.after(7000, on_completion)  # 3s countdown + 3s recording + 1s buffer

    def create_manage_gestures_tab_OLD(self, parent):
        """Create manage gestures tab"""
        # Title
        title_label = ttk.Label(parent, text="📋 Manage Profile Gestures",
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Current profile display
        current_frame = ttk.Frame(parent)
        current_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(current_frame, text="Managing Profile:",
                 font=('Arial', 12, 'bold')).pack(side='left')

        self.manage_profile_label = ttk.Label(current_frame,
                                             text=self.profile_manager.current_profile or "No profile selected",
                                             font=('Arial', 12), foreground='blue')
        self.manage_profile_label.pack(side='left', padx=(10, 0))

        # Gestures list
        list_frame = ttk.LabelFrame(parent, text="Profile Gestures", padding=10)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Create treeview for gestures
        columns = ('Name', 'Key Binding', 'Status', 'Type')
        self.gesture_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)

        # Define headings
        self.gesture_tree.heading('Name', text='Gesture Name')
        self.gesture_tree.heading('Key Binding', text='Key Binding')
        self.gesture_tree.heading('Status', text='Status')
        self.gesture_tree.heading('Type', text='Hand Type')

        # Configure column widths
        self.gesture_tree.column('Name', width=150)
        self.gesture_tree.column('Key Binding', width=100)
        self.gesture_tree.column('Status', width=80)
        self.gesture_tree.column('Type', width=100)

        # Scrollbar for treeview
        tree_scrollbar = ttk.Scrollbar(list_frame, orient='vertical',
                                      command=self.gesture_tree.yview)
        self.gesture_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.gesture_tree.pack(side='left', fill='both', expand=True)
        tree_scrollbar.pack(side='right', fill='y')

        # Management buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="✅ Activate",
                  command=self.activate_selected_gesture).pack(side='left', padx=5)

        ttk.Button(button_frame, text="❌ Deactivate",
                  command=self.deactivate_selected_gesture).pack(side='left', padx=5)

        ttk.Button(button_frame, text="✏️ Edit Binding",
                  command=self.edit_gesture_binding).pack(side='left', padx=5)

        ttk.Button(button_frame, text="🗑️ Delete",
                  command=self.delete_selected_gesture).pack(side='left', padx=5)

        ttk.Button(button_frame, text="🔄 Refresh",
                  command=self.refresh_gesture_list).pack(side='left', padx=5)

        # Initial refresh
        self.refresh_gesture_list()

    def create_new_profile_dialog(self):
        """Create dialog for new profile creation"""
        dialog = tk.Toplevel(self.settings_window)
        dialog.title("Create New Profile")
        dialog.geometry("400x300")
        dialog.transient(self.settings_window)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")

        # Profile name
        ttk.Label(dialog, text="Profile Name:", font=('Arial', 12, 'bold')).pack(pady=10)
        name_entry = ttk.Entry(dialog, width=30, font=('Arial', 12))
        name_entry.pack(pady=5)

        # Profile description
        ttk.Label(dialog, text="Description:", font=('Arial', 12, 'bold')).pack(pady=(20, 5))
        desc_text = tk.Text(dialog, width=40, height=5, font=('Arial', 10))
        desc_text.pack(pady=5)

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)

        def create_profile():
            name = name_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()

            if not name:
                messagebox.showerror("Error", "Please enter a profile name")
                return

            if name in self.profile_manager.get_profile_names():
                messagebox.showerror("Error", "Profile name already exists")
                return

            if self.profile_manager.create_profile(name, description):
                messagebox.showinfo("Success", f"Profile '{name}' created successfully!")
                self.refresh_profile_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to create profile")

        ttk.Button(button_frame, text="Create", command=create_profile).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=10)

        name_entry.focus()

    def create_template_profile(self, template_name):
        """Create template profiles with predefined gestures"""
        # Check if profile already exists
        if template_name in self.profile_manager.get_profile_names():
            result = messagebox.askyesno("Profile Exists",
                                       f"Profile '{template_name}' already exists. Replace it?")
            if not result:
                return
            self.profile_manager.delete_profile(template_name)

        # Create the profile using the profile manager's template method
        if self.profile_manager.create_template_profile(template_name):
            messagebox.showinfo("Success", f"Template '{template_name}' created successfully!\n\n"
                                         "Note: You'll need to record gestures for each action.")
            self.refresh_profile_list()
        else:
            messagebox.showerror("Error", "Failed to create template profile")

    def load_selected_profile(self):
        """Load the selected profile from the list"""
        selection = self.profile_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a profile to load")
            return

        profile_name = self.profile_listbox.get(selection[0])

        if self.profile_manager.load_profile(profile_name):
            messagebox.showinfo("Success", f"Profile '{profile_name}' loaded successfully!")
            self.update_profile_labels()
            self.refresh_gesture_list()
            self.refresh_template_gestures()
        else:
            messagebox.showerror("Error", "Failed to load profile")

    def delete_selected_profile(self):
        """Delete the selected profile"""
        selection = self.profile_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a profile to delete")
            return

        profile_name = self.profile_listbox.get(selection[0])

        result = messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete profile '{profile_name}'?")
        if result:
            if self.profile_manager.delete_profile(profile_name):
                messagebox.showinfo("Success", f"Profile '{profile_name}' deleted successfully!")
                self.refresh_profile_list()
                self.update_profile_labels()
            else:
                messagebox.showerror("Error", "Failed to delete profile")

    def refresh_profile_list(self):
        """Refresh the profile list"""
        if self.profile_listbox:
            self.profile_listbox.delete(0, tk.END)
            for profile_name in self.profile_manager.get_profile_names():
                self.profile_listbox.insert(tk.END, profile_name)

    def update_profile_labels(self):
        """Update profile labels in the UI"""
        current_profile = self.profile_manager.current_profile or "None Selected"

        if hasattr(self, 'current_profile_label') and self.current_profile_label:
            self.current_profile_label.config(text=current_profile)

        # Update dropdown selection
        if hasattr(self, 'profile_var') and self.profile_manager.current_profile:
            self.profile_var.set(self.profile_manager.current_profile)

    def refresh_gesture_list(self):
        """Refresh the gesture list"""
        if not hasattr(self, 'gesture_tree') or not self.gesture_tree:
            return

        # Clear existing items
        for item in self.gesture_tree.get_children():
            self.gesture_tree.delete(item)

        # Add gestures from current profile
        if self.profile_manager.current_profile:
            profile_data = self.profile_manager.get_current_profile_data()
            if profile_data:
                gestures = profile_data.get('gestures', {})
                bindings = profile_data.get('bindings', {})

                for gesture_name, gesture_data in gestures.items():
                    key_binding = bindings.get(gesture_name, "Not set")
                    hand_type = gesture_data.get('hand_type', 'single')
                    hand_type_display = "👥 Both" if hand_type == "both" else "👤 Single"
                    self.gesture_tree.insert('', 'end', values=(gesture_name, key_binding, hand_type_display))

    # Individual gesture activation removed - now using profile-level activation

    def edit_gesture_binding(self):
        """Edit the key binding for selected gesture"""
        selection = self.gesture_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a gesture to edit")
            return

        item = self.gesture_tree.item(selection[0])
        gesture_name = item['values'][0]
        current_binding = item['values'][1]

        new_binding = simpledialog.askstring("Edit Key Binding",
                                            f"Enter new key binding for '{gesture_name}':",
                                            initialvalue=current_binding)

        if new_binding:
            profile_data = self.profile_manager.get_current_profile_data()
            if profile_data:
                profile_data.setdefault('bindings', {})[gesture_name] = new_binding
                self.profile_manager.save_profile(self.profile_manager.current_profile, profile_data)
                self.refresh_gesture_list()
                messagebox.showinfo("Success", f"Key binding updated for '{gesture_name}'")

    def delete_selected_gesture(self):
        """Delete the selected gesture"""
        selection = self.gesture_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a gesture to delete")
            return

        item = self.gesture_tree.item(selection[0])
        gesture_name = item['values'][0]

        result = messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete gesture '{gesture_name}'?")
        if result:
            profile_data = self.profile_manager.get_current_profile_data()
            if profile_data:
                # Remove from all dictionaries
                profile_data.get('gestures', {}).pop(gesture_name, None)
                profile_data.get('bindings', {}).pop(gesture_name, None)
                active_gestures = profile_data.get('active_gestures', [])
                if gesture_name in active_gestures:
                    active_gestures.remove(gesture_name)

                self.profile_manager.save_profile(self.profile_manager.current_profile, profile_data)
                self.refresh_gesture_list()
                messagebox.showinfo("Success", f"Gesture '{gesture_name}' deleted")

    def close_settings_window(self):
        """Close the settings window"""
        self.settings_open = False
        if self.settings_window:
            self.settings_window.destroy()
            self.settings_window = None

    def update_tkinter(self):
        """Update tkinter GUI (thread-safe)"""
        if hasattr(self, 'root') and self.root:
            try:
                # Only update if we're in the main thread
                self.root.update_idletasks()
                self.root.update()
            except Exception as e:
                # Silently handle GUI update errors to prevent crashes
                pass

        # Also update settings window if open
        if hasattr(self, 'settings_window') and self.settings_window:
            try:
                self.settings_window.update_idletasks()
            except Exception as e:
                pass

    def cleanup(self):
        """Cleanup GUI resources"""
        if hasattr(self, 'root') and self.root:
            try:
                self.root.destroy()
            except:
                pass
