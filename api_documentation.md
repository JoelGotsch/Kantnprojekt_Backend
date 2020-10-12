# API Documentation Kantnprojekt v0_1

## header description:

## authentication:

### Exercise

#### get exercise/<exercise_id>
- special case exercise_id=all returns a list of all exercises for that user (common exercises + the ones created by user).
- example:

```
{"name": "exercise_name",
 "unit": "hours"
 "points": 10
``` 

#### post exercise

#### delete exercise

### Workout

#### get workout/<workout_id>, workout/<start_date:?end_date>
- special case exercise_id=all returns a list of all exercises for that user (common exercises + the ones created by user).
- example:

```
{"name": "exercise_name",
 "unit": "hours"
 "points": 10
``` 

#### post workout

#### delete workout/<workout_id>


### Challenge

#### get challenge<challenge_id>, challenge<start_date:?end_date>
- special case challenge_id=all returns a list of all challenges.
- example:

```
{"name": "exercise_name",
 "unit": "hours"
 "points": 10
``` 

#### post challenge

#### post challenge/join<challenge_id>

#### post challenge/leave<challenge_id>

#### delete challenge/<challenge_id>

### Friend

#### get friend<user_id>

#### delete friend<user_id>

