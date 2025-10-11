import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
from pathlib import Path
import json


def main():
    # 1. Initialize GLFW
    if not glfw.init():
        raise Exception("Could not initialize GLFW")

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1920, 1080, "ImGui Example Window/App", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Could not create GLFW window")

    # Make the window's context current
    glfw.make_context_current(window)

    # 2. Create ImGui context
    imgui.create_context()

    # 3. Setup ImGui GLFW + OpenGL renderer
    impl = GlfwRenderer(window)

    # Start in light mode
    style = imgui.get_style()
    imgui.style_colors_light(style)

    # Buffer for input text
    MAX_LEN = 256
    new_item_buffer = "\0" * MAX_LEN # buffer of 256 null characters

    def todo_data_formatted(todo_data): # function to format todo data for display
        # converts the json dictionaries to string for display in window
        if not todo_data: # check if empty
            return "Your To-Do list is empty."
        formatted_lines = []
        for i, task_item in enumerate(todo_data): # iterate through each task dictionary
            status = "[x]" if task_item.get("done", False) else "[ ]" # check if done
            task_text = task_item.get("task", "untitled task") # get task text if key is missing
            formatted_lines.append(f"{i + 1}. {status} {task_text}") # format line
        return "\n".join(formatted_lines)

    display_string = "" 

    # Main loop
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()
        impl.process_inputs()

        # Start new ImGui frame
        imgui.new_frame()

        # Fullscreen main window
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(1920, 1080)

        # Create main window with menu bar and tabs
        if imgui.begin("Main Window", flags=imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_TITLE_BAR):
            # ===== MENU BAR =====
            if imgui.begin_menu_bar():
                if imgui.begin_menu("File", True):
                    if imgui.menu_item("Open")[0]:
                        print("Open clicked")
                    if imgui.menu_item("Save")[0]:
                        print("Save clicked")
                    imgui.separator()
                    if imgui.menu_item("Exit")[0]:
                        glfw.set_window_should_close(window, True)
                    imgui.end_menu()

                if imgui.begin_menu("Edit", True):
                    if imgui.menu_item("Undo")[0]:
                        print("Undo clicked")
                    if imgui.menu_item("Redo")[0]:
                        print("Redo clicked")
                    imgui.end_menu()

                if imgui.begin_menu("Help", True):
                    if imgui.menu_item("About")[0]:
                        print("About clicked")
                    imgui.end_menu()

                imgui.end_menu_bar()
            # ===== END MENU BAR =====

            # ===== TAB BAR =====
            if imgui.begin_tab_bar("MainTabs"):

                # --- Home Tab ---
                if imgui.begin_tab_item("Home")[0]:
                    imgui.text("Add to or read your to do list here.")
                    imgui.separator()

                    # input field and uppdate buffer every frame
                    _, new_item_buffer = imgui.input_text("New todo item", new_item_buffer, MAX_LEN)

                    if imgui.button("Load to do list"):
                        if Path("todo.json").is_file(): # Check if file exists
                            with open("todo.json", "r") as f:
                                todo_data = json.load(f)

                                display_string = todo_data_formatted(todo_data) # format the data for display
                        else:
                            todo_data = []

                    #imgui.separator()

                    if imgui.button("Save to do list"):
                        new_item_text = new_item_buffer.split("\0", 1)[0].strip() # Get string up to first null character and strip whitespace

                        if new_item_text: # check if input is not empty
                            new_task = {"task": new_item_text, "done": False}
                            todo_data.append(new_task)

                            with open("todo.json", "w") as f:
                                json.dump(todo_data, f, indent=4) # dump full list
                                new_item_buffer = "\0" * MAX_LEN # Clear input buffer

                    #imgui.text_colored("", 0.0, 0.9, 0.6)
                    imgui.separator()
                    
                    imgui.text(display_string)

                    imgui.end_tab_item()

                # --- Settings Tab ---
                if imgui.begin_tab_item("Settings")[0]:
                    imgui.text("Settings Tab")
                    changed, value = imgui.checkbox("Enable feature", False)
                    if changed:
                        print(f"Feature enabled: {value}")

                    # Light Mode Button
                    if imgui.button("Light Mode"):
                        imgui.style_colors_light(style)
                        print("Changed to light mode!")

                    # Dark Mode Button
                    if imgui.button("Dark Mode"):
                        imgui.style_colors_dark(style)
                        print("Changed to dark mode!")

                    imgui.end_tab_item()

                # --- About Tab ---
                if imgui.begin_tab_item("About")[0]:
                    imgui.text("This is a demo ImGui app.")
                    imgui.end_tab_item()

                imgui.end_tab_bar()
            # ===== END TAB BAR =====

            imgui.end()  # End main window

        # Render ImGui
        imgui.render()
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)  # White background
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        impl.render(imgui.get_draw_data())

        # Swap front and back buffers
        glfw.swap_buffers(window)

    # Cleanup
    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()