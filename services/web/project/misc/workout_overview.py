
from datetime import datetime, timedelta

from sqlalchemy.sql.elements import Null
from ..misc import funcs as funcs
import functools

class DailyOverview:
    
    def __init__(self, date):
        try:
            year = date.year()
        except Exception as e:
            year = date.year
        try:
            month = date.month()
        except Exception as e:
            month = date.month
        try:
            day = date.day()
        except Exception as e:
            day = date.day
        clean_date = datetime(year, month, day)
        self.date = clean_date
        self.pointsPerExercise = {}
        self.countsPerExercise = {}
        self.pointsPerExerciseWeek = {}
        self.countsPerExerciseWeek = {}


    def calcTotalPoints(self):
        return(functools.reduce(lambda a,b : a+b, self.pointsPerExercise.values()))
    
    def serialize(self):
        if len(self.pointsPerExercise) > 0:
            return({self.date.strftime("%Y-%m-%d"): self.calcTotalPoints()})
        else:
            return(None)

    def addAction(self, ac, ex, week_only = False):
        if not ex.exercise_id in self.pointsPerExerciseWeek:
            self.countsPerExerciseWeek[ex.exercise_id] = 0
            self.pointsPerExerciseWeek[ex.exercise_id] = 0
            self.countsPerExercise[ex.exercise_id] = 0
            self.pointsPerExercise[ex.exercise_id] = 0

        daily_count = ac.number
        # print("week only = " + str(week_only))
        if self.countsPerExerciseWeek[ex.exercise_id] +ac.number > ex.weekly_allowance > 0:
            daily_count = max(ex.weekly_allowance-self.countsPerExerciseWeek[ex.exercise_id]-daily_count, 0)

        if self.countsPerExercise[ex.exercise_id] +daily_count > ex.daily_allowance > 0:
            daily_count = max(ex.daily_allowance-self.countsPerExercise[ex.exercise_id]-daily_count, 0)
        
        daily_points = daily_count * ex.points
        if ex.max_points_day > 0:
            daily_points = min(daily_points, ex.max_points_day)
        if ex.max_points_week > 0:
            daily_points = min(daily_points, ex.max_points_week - self.pointsPerExerciseWeek[ex.exercise_id])

        self.countsPerExerciseWeek[ex.exercise_id] += ac.number
        self.pointsPerExerciseWeek[ex.exercise_id] += daily_points

        if not week_only:
            self.countsPerExercise[ex.exercise_id] += ac.number
            self.pointsPerExercise[ex.exercise_id] += daily_points

class WorkoutOverviews:
    def __init__(self, exercises):
        self.exercises = exercises
        self.dailyOverviews = {}

    def addWorkout(self, wo):
        for ac in wo.actions:
            self.addAction(ac, wo.date)
    
    def addAction(self, ac, date):
        try:
            wday = date.weekday()
        except Exception as e:
            wday = date.weekday
        weekday = int(wday)
        daywynr = funcs.dayWeekYearNr(date)
        try:
            ex = self.exercises[ac.exercise_id]
        except Exception as e:
            # print("ERROR: Couldn't find exercise_id " + ac.exercise_id + " in exercises.")
            return()
        i = 0
        while weekday + i < 7:
            if daywynr in self.dailyOverviews.keys():
                dailyOv = self.dailyOverviews[daywynr]
                # print("Accessed again DailyOverview "+str(daywynr))
            else:
                dailyOv = DailyOverview(date+timedelta(days=i))
                self.dailyOverviews[daywynr] = dailyOv
                # print("Created new DailyOverview "+str(daywynr))
            dailyOv.addAction(ac, ex, week_only=(i!=0))
            # print(dailyOv.calcTotalPoints())
            # self.dailyOverviews[daywynr] = dailyOv
            i+=1
            daywynr+=1

    def serialize(self):
        print(self.dailyOverviews.values())
        return_dict = {dailyOverv.date.strftime("%Y-%m-%d"): {"points": dailyOverv.calcTotalPoints(), "date": dailyOverv.date.isoformat()} for dailyOverv in self.dailyOverviews.values() if dailyOverv.calcTotalPoints()!=0}
        return(return_dict)

def calcWorkoutsDict(exercises, workouts, latest_edit):
    # exercises must be dict containing all challenge-exercises with keys = exercise ids.
    # workouts must be a list/iterable of all workouts of the user
    # returns dict of workouts (workouts are filtered: only days are included which are after the oldest workout that was created/edited after latest_edit)
    # keys of the dict: day in format "%Y-%m-%d"


        #sort workouts according to their date
        # do each week independently, starting with week of earliest workout changed since refresh_date
        # make cumulative dict as well as day per day
        # sum up per day (reduce?)

        #return day-per-day dicts

    # calculate the monday 0 am before latest_edit date
    weekstart_of_latest_edit = funcs.calc_weekstart(latest_edit)
    
    # filter and sort workouts:
    workouts_dict = {wo.date.isoformat(): wo for wo in workouts if wo.date>= weekstart_of_latest_edit}
    # test = workouts_dict.values()
    # test2 = workouts_dict.items()
    # test3 = [wo.date for wo in workouts_dict.values()]

    # def sortDate(s):
    #     return(s.date)
    workouts_list = [value for (key, value) in  sorted(workouts_dict.items(), key=lambda x: x[1].date)]#returns sorted list
    
    #make sure exercises is a dict with exercise_id´s as keys!


    #for each week:
    # for each exercise_id
    woOverview = WorkoutOverviews(exercises)
    for wo in workouts_list:
        if wo.date < weekstart_of_latest_edit:
            next
        # wo_date = wo.date.strftime("%Y-%m-%d")
        woOverview.addWorkout(wo)
    return(woOverview.serialize())
