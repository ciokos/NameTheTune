from tkinter import *
import threading
import random
import queue
import socket


class GuiPart:
    def __init__(self, master, queue, exitClick, readyClick, state):
        self.queue = queue

        self.state = StringVar()
        self.state.set(state)

        # Set up the GUI
        tFrame = Frame(master).pack(side=TOP)
        state_label = Label(tFrame, textvariable=self.state)
        ready_btn = Button(master, text='Ready', command=readyClick, width=10, height=2)
        exit_btn = Button(master, text="Exit", command=exitClick, width=10, height=2)
        state_label.pack(side=TOP)
        ready_btn.place(x=220, y=110)
        exit_btn.place(x=0, y=110)
        master.geometry("300x150")
        master.title("Name That Tune")

        # Add more GUI stuff here depending on your specific needs

    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                self.state.set(msg)

            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Init socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "10.0.0.22"

        port = 9999

        self.socket.connect((host, port))

        state = self.socket.recv(1024)
        state = state.decode("ascii")

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication,self.ready, state)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """

        alt = 0
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
            msg = self.socket.recv(1024)
            msg = msg.decode("ascii")
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0
        self.socket.close()

    def ready(self):
        text = 'ready'
        self.socket.send(text.encode('ascii'))



rand = random.Random()
root = Tk()

client = ThreadedClient(root)
root.mainloop()
