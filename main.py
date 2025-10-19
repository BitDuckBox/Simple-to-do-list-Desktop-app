import glfw, OpenGL.GL as gl, imgui, json, time
from imgui.integrations.glfw import GlfwRenderer
from pathlib import Path

fileName="todo.json"
maxLen=256
showPerf=False

def loadTodo():
    return json.loads(Path(fileName).read_text()) if Path(fileName).is_file() else []

def saveTodo(todoList):
    Path(fileName).write_text(json.dumps(todoList,indent=4))

def main():
    global showPerf
    if not glfw.init(): raise Exception("GLFW init fail")
    width,height=1280,720
    window=glfw.create_window(width,height,"todoapp",None,None)
    if not window: glfw.terminate(); raise Exception("window fail")
    glfw.make_context_current(window)
    imgui.create_context()
    impl=GlfwRenderer(window)
    style=imgui.get_style(); imgui.style_colors_dark(style)
    style.window_rounding=12; style.frame_rounding=8; style.scrollbar_rounding=6
    style.window_padding=(10,10); style.item_spacing=(4,4); style.frame_padding=(8,4)
    io=imgui.get_io(); defaultFont=io.fonts.add_font_default(); io.font_global_scale=1.1; impl.refresh_font_texture()
    buffer="\0"*maxLen
    todoList=loadTodo()
    lastTime=time.time(); fps=0

    while not glfw.window_should_close(window):
        glfw.poll_events(); impl.process_inputs()
        if glfw.get_key(window,glfw.KEY_M)==glfw.PRESS: showPerf=not showPerf
        frameStart=time.time()
        imgui.new_frame()
        imgui.set_next_window_position(0,0); imgui.set_next_window_size(width,height)
        if imgui.begin("todoapp",flags=imgui.WINDOW_NO_TITLE_BAR|imgui.WINDOW_MENU_BAR):
            if imgui.begin_menu_bar():
                if imgui.begin_menu("file",True):
                    if imgui.menu_item("load")[0]: todoList=loadTodo()
                    if imgui.menu_item("save")[0]: saveTodo(todoList)
                    if imgui.menu_item("exit")[0]: glfw.set_window_should_close(window,True)
                    imgui.end_menu()
                if imgui.begin_menu("help",True):
                    if imgui.menu_item("about")[0]: print("todoapp v3")
                    imgui.end_menu()
                imgui.end_menu_bar()

            if imgui.begin_tab_bar("tabs"):
                if imgui.begin_tab_item("home")[0]:
                    imgui.push_font(defaultFont); imgui.text_colored("📝 todo",0.2,0.7,0.9); imgui.pop_font(); imgui.separator()
                    changed, buffer=imgui.input_text("##input",buffer,maxLen,imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
                    imgui.same_line()
                    if imgui.button("add",80,25) or (changed and buffer.strip()!=""):
                        taskText=buffer.split("\0",1)[0].strip()
                        if taskText: todoList.append({"task":taskText,"done":False}); buffer="\0"*maxLen; saveTodo(todoList)
                    imgui.begin_child("list",0,400,border=True)
                    for i,item in enumerate(todoList):
                        changed,item["done"]=imgui.checkbox(item["task"],item["done"])
                        if changed: saveTodo(todoList)
                        imgui.same_line()
                        imgui.push_style_var(imgui.STYLE_FRAME_PADDING,(2,1))
                        if imgui.button(f"del##{i}",60,22): todoList.pop(i); saveTodo(todoList); imgui.pop_style_var(); break
                        imgui.pop_style_var()
                    imgui.end_child(); imgui.end_tab_item()

                if imgui.begin_tab_item("settings")[0]:
                    if imgui.button("light",100,25): imgui.style_colors_light(style)
                    imgui.same_line()
                    if imgui.button("dark",100,25): imgui.style_colors_dark(style)
                    imgui.end_tab_item()

                if imgui.begin_tab_item("about")[0]:
                    imgui.text_colored("todoapp v3",0.2,0.7,0.9); imgui.separator()
                    imgui.bullet_text("add/check/uncheck/delete tasks"); imgui.bullet_text("light/dark mode"); imgui.bullet_text("persistent storage")
                    imgui.end_tab_item()
                imgui.end_tab_bar()

            if showPerf:
                now=time.time(); fps=1/(now-lastTime); lastTime=now
                imgui.set_next_window_position(10,10); imgui.set_next_window_size(160,50,imgui.ALWAYS_CONDITION)
                imgui.begin("perf",flags=imgui.WINDOW_NO_TITLE_BAR|imgui.WINDOW_NO_RESIZE|imgui.WINDOW_NO_MOVE)
                imgui.text(f"fps: {fps:.1f}"); imgui.text(f"frame: {(1000*(time.time()-frameStart)):.2f}ms")
                imgui.end()
            imgui.end()

        imgui.render(); gl.glClearColor(0.1,0.1,0.15,1); gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        impl.render(imgui.get_draw_data()); glfw.swap_buffers(window)

    impl.shutdown(); glfw.terminate()

if __name__=="__main__": main()
