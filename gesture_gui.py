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

        # Create notebook for tabs
        notebook = ttk.Notebook(self.settings_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab 1: Profile Management
        profile_frame = ttk.Frame(notebook)
        notebook.add(profile_frame, text="📁 Profile Management")
        self.create_profile_management_tab(profile_frame)

        # Tab 2: Add Gesture to Profile
        add_gesture_frame = ttk.Frame(notebook)
        notebook.add(add_gesture_frame, text="➕ Add Gesture")
        self.create_add_gesture_tab(add_gesture_frame)

        # Tab 3: Manage Profile Gestures
        manage_frame = ttk.Frame(notebook)
        notebook.add(manage_frame, text="📋 Manage Gestures")
        self.create_manage_gestures_tab(manage_frame)
    
    def create_profile_management_tab(self, parent):
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
    
    def create_add_gesture_tab(self, parent):
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
                self.recording_status_label.config(text=message, foreground=color)
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
                self.record_button.config(state='normal', text="🔴 Start Recording")
            if hasattr(self, 'recording_status_label') and self.recording_status_label:
                self.recording_status_label.config(text="Ready to record gesture", foreground='black')
        except Exception as e:
            print(f"Warning: Could not reset GUI elements: {e}")
    
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

    def create_manage_gestures_tab(self, parent):
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
        current_profile = self.profile_manager.current_profile or "None"

        if hasattr(self, 'current_profile_label') and self.current_profile_label:
            self.current_profile_label.config(text=current_profile)
        if hasattr(self, 'selected_profile_label') and self.selected_profile_label:
            self.selected_profile_label.config(text=current_profile)
        if hasattr(self, 'manage_profile_label') and self.manage_profile_label:
            self.manage_profile_label.config(text=current_profile)

    def refresh_gesture_list(self):
        """Refresh the gesture list in manage tab"""
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
                active_gestures = set(profile_data.get('active_gestures', []))

                for gesture_name, gesture_data in gestures.items():
                    key_binding = bindings.get(gesture_name, "Not set")
                    status = "Active" if gesture_name in active_gestures else "Inactive"
                    hand_type = gesture_data.get('hand_type', 'single')

                    self.gesture_tree.insert('', 'end', values=(gesture_name, key_binding, status, hand_type))

    def activate_selected_gesture(self):
        """Activate the selected gesture"""
        selection = self.gesture_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a gesture to activate")
            return

        item = self.gesture_tree.item(selection[0])
        gesture_name = item['values'][0]

        profile_data = self.profile_manager.get_current_profile_data()
        if profile_data:
            if gesture_name not in profile_data.get('active_gestures', []):
                profile_data.setdefault('active_gestures', []).append(gesture_name)
                self.profile_manager.save_profile(self.profile_manager.current_profile, profile_data)

            self.refresh_gesture_list()
            messagebox.showinfo("Success", f"Gesture '{gesture_name}' activated")

    def deactivate_selected_gesture(self):
        """Deactivate the selected gesture"""
        selection = self.gesture_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a gesture to deactivate")
            return

        item = self.gesture_tree.item(selection[0])
        gesture_name = item['values'][0]

        profile_data = self.profile_manager.get_current_profile_data()
        if profile_data:
            active_gestures = profile_data.get('active_gestures', [])
            if gesture_name in active_gestures:
                active_gestures.remove(gesture_name)
                self.profile_manager.save_profile(self.profile_manager.current_profile, profile_data)

            self.refresh_gesture_list()
            messagebox.showinfo("Success", f"Gesture '{gesture_name}' deactivated")

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
