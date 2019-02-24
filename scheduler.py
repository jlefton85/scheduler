import random
import tkinter as tk
import texttable as tt
from tkinter.font import Font

class Lad:
    def __init__(self, name):
        self.name = name
        self.timesWorked = [0] * 7
        self.daysAbsent = [0] * 7

class DefaultFrame(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.frame = tk.Frame(window)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

class DaysFrame:
    def __init__(self):
        self.frame = DefaultFrame()
        self.title = tk.Label(self.frame, text="Which days do you need scheduling for?", font=font)
        self.title.grid(row=0, column=1)
        self.vars = [tk.IntVar() for x in range(7)]
        self.options = tk.Frame(self.frame)
        self.options.grid(row=1, column=1)
        for num in range(7):
            button = tk.Checkbutton(self.options, variable=self.vars[num], text=days[num], width=16, height=4, font=smallFont)
            button.grid(row=0, column=num)
            self.vars[num].set(0)
        self.frame.grid(row=0, column=1)
        self.submit = tk.Button(self.frame, text="Submit", command=self.command)
        self.submit.grid(row=2, column=1)

    def command(self):
        self.frame.grid_remove()
        global numDays
        global daysActive
        global absentFrames
        for day in self.vars:
            numDays += day.get()
        daysActive = [days[num] for num in range(len(days)) if self.vars[num].get() == 1]
        absentFrames = [AbsentFrame(num) for num in range(len(days)) if self.vars[num].get() == 1]
        absentFrames[0].frame.grid(row=0, column=1)
        AbsentFrame.numDaysAbsent = numDays

class AbsentFrame:
    numDaysAbsent = 0

    def __init__(self, day):
        self.day = days[day]
        self.frame = DefaultFrame()
        self.title = tk.Label(self.frame, text="Who will be absent on " + self.day + "?", font=font)
        self.title.grid(row=0, column=1)
        self.vars = [tk.IntVar() for x in range(len(lads))]
        self.options = tk.Frame(self.frame)
        for num in range(len(lads)):
            button = tk.Checkbutton(self.options, variable=self.vars[num], text=lads[num].name, width=16, height=4, font=smallFont)
            button.grid(row=num % 3, column=num // 3)
        self.options.grid(row=1, column=1)
        self.submit = tk.Button(self.frame, text="Submit", command=self.command)
        self.submit.grid(row=2, column=1)

    def clear(self):
        for box in range(len(self.vars)):
            self.vars[box].set(0)

    def command(self):
        AbsentFrame.numDaysAbsent -= 1
        for x in range(len(self.vars)):
            lads[x].daysAbsent[days.index(self.day)] = self.vars[x].get()
        self.frame.grid_remove()
        if AbsentFrame.numDaysAbsent > 0:
            absentFrames[numDays - AbsentFrame.numDaysAbsent].clear()
            absentFrames[numDays - AbsentFrame.numDaysAbsent].frame.grid(row=0, column=1)
        else:
            scheduleFrames = [ScheduleFrame(day) for day in range(len(daysActive))]
            for frame in range(len(scheduleFrames)):
                scheduleFrames[frame].frame.grid()


class ScheduleFrame:
    def __init__(self, day):
        self.day = day
        self.frame = DefaultFrame()
        self.title = tk.Label(self.frame, text=daysActive[self.day], font=font)
        self.title.grid(row=0, column=1)
        self.presentLads = [lads[x] for x in range(len(lads)) if lads[x].daysAbsent[day] == 0]
        self.assignedJobs = [[]] * 21
        self.schedule = tk.Label(self.frame, text=self.createTable(), font=smallFont)
        self.schedule.grid(row=1, column=1)

    def assignJob(self, job, numLads):
        chosenLads = []
        while len(chosenLads) < numLads:
            chosenLad = self.presentLads[random.randint(0, len(self.presentLads) - 1)]
            if chosenLad.timesWorked[job % 3] < numDays * (shiftsPerDay[job % 3] / 5.0):
                alreadyWorking = [self.assignedJobs[(job // 7) * 7 + num] for num in range(len(jobs))]
                working = 0
                for shiftJob in alreadyWorking:
                    if chosenLad in shiftJob:
                        working = 1
                if not working and chosenLad not in chosenLads:
                    chosenLads.append(chosenLad)
                    chosenLad.timesWorked[job % 3] += 1
        return chosenLads

    def assignJobs(self):
        ladsPerShift = [3, 1, 1, 3, 1, 1, 1] * 3
        ladsPerShift[14] = 1
        ladsPerShift[17] = 1
        for x in range(len(ladsPerShift)):
            self.assignedJobs[x] = self.assignJob(x, ladsPerShift[x])

    def createTable(self):
        self.assignJobs()
        table = tt.Texttable(max_width=200)
        table.add_row(["Time"] + [job for job in jobs])
        ladsPerShift = [3, 1, 1, 3, 1, 1, 1] * 3
        ladsPerShift[14] = 1
        ladsPerShift[17] = 1
        for time in range(3):
            table.add_row([times[time]] + [extractNames(self.assignedJobs[time * 7 + job]) for job in range(len(jobs))])
        print(table.draw())
        return table.draw()

def extractNames(group):
    ret = ""
    for lad in group:
        ret = ret + lad.name + ", "
    ret = ret[:len(ret) - 2]
    return ret

def assignTime(group, numLads):
    return [group[lad] for lad in range(numLads)]


names = [
    "Chris Mannino",
    "Rory McNabb",
    "Alejandro Serrano",
    "Jackson Seely",
    "Josh Gould",
    "Will Wilson",
    "Reed Wilson",
    "Jack Bolster",
    "Chodis",
    "Yegor",
    "Joe",
    "Trevor",
    "Ryan Walsh",
    "Will Minichino",
    "Paulo Ferreira",
    "Alex Province",
    "Matt",
    "Connor Willey",
    "Brian Peoples",
    "Phil",
    "Matt Flaherty"
]

lads = [Lad(name) for name in names]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

jobs = ["Ashtray", "First Floor Fire", "Bathroom", "North Stairs", "South Stairs", "Upstairs Fire", "DJ Booth"]

times = ["First Shift", "Second Shift", "Third Shift"]

shiftsPerDay = [7, 3, 3, 7, 3, 3, 3]

numDays = 0

def main():
    global window
    window = tk.Tk()
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(2, weight=1)
    width, height = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (width, height))
    global font
    global smallFont
    font = Font(family="Courier", size=16)
    smallFont = Font(family="Courier", size=10)
    window.title("Scheduler")

    daysFrame = DaysFrame()
    daysFrame.frame.grid(row=0, column=1)

    window.mainloop()

main()