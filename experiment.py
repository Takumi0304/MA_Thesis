#!/usr/bin/env python3

WITH_EYETRACKER = False

# Load Chamois:
exec(open("chamois.py").read())



if WITH_EYETRACKER:
    exec(open("TPx.py").read())  # Eye-Trackerが必要な場合にTPx.pyを読み込む

# Structure of the experiment: eye-trackerと繋がっている・繋がっていない時の分岐
#if WITH_EYETRACKER:
#    tpx = TPx()  # Eye-Trackerがある場合はTPxオブジェクトを作成
#else:
#    tpx = None  # Eye-Trackerがない場合はNoneを設定

# Change theme:
theme('Black')

font = "Courier"
fontsize = 22
wordspacing = 10

# Load stimuli:
practice_sentences = load_stimuli("practice_sentences.tsv")
target_sentences = load_stimuli("target_sentences.tsv")
filler_sentences = load_stimuli("filler_sentences.tsv")

# Mix and shuffle:
stimuli = next_latin_square_list(target_sentences)
stimuli += filler_sentences
random.shuffle(stimuli)

# Structure of the experiment:
if WITH_EYETRACKER:
    tpx = TPx()

# An experiment consists of a series of pages:
pages = []

# Welcome screen:
pages.append(ConsentForm("""
  Thank you very much for participating in this experiment!

  In this experiment, you will read English sentences and answer questions related to their contents. 
  Your eye movements will be tracked by a camera. 

  There are no known risks or side effects associated with this procedure. 
  Please avoid moving your head during the experiment.

  Your cooperation is essential for the success of this study, 
  so we kindly ask you to concentrate throughout the experiment.

  All collected data will be anonymized and used solely for the purpose of this study.
"""))

# Calibration:
if WITH_EYETRACKER:
    pages.append(CenteredInstructions("Before starting the experiment, we need to calibrate the Eye-Tracker."))
    pages.append(TPxCalibration(tpx))

# Explain practice sentences:
pages.append(CenteredInstructions("""
  First, let us practice with some sentences to help you understand how the experiment will proceed.

  The procedure is as follows:
  1. Please look at the blinking circle that appears on the left side of the screen.
  2. Then, read the sentence at your own pace, trying to understand its meaning.
  3. When you have finished reading, look at the circle in the bottom-right corner to proceed to the next screen.
  4. You will then see a "Yes/No" question. To answer, press the "J" key for "Yes" and the "F" key for "No."

  Please keep your right index finger on the "J" key and your left index finger on the "F" key 
  to avoid having to search for the keys when the question appears. 
  Remember not to move your head during the experiment.
"""))

for i,c,s,q in practice_sentences:
  if WITH_EYETRACKER:
    pages.append(TPxReadingTrial(i,c,s,tpx))
  else:
    pages.append(ReadingTrial(i,c,s))
  pages.append(YesNoQuestionTrial(i,c,q))
  pages.append(TPxNext(tpx))
pages.pop()

# Explain experimental trials:
pages.append(CenteredInstructions("""
  Great! Now let's proceed to the main part, which will take a bit longer.

  The procedure is the same, but the questions will appear only after several sentences.

  You may take a break at any time, but it's best to do so after completing a sentence or question.
  Please place your fingers on the "F" and "J" keys.
"""))

# Experimental trials:
for i,c,s,q in stimuli:
  if WITH_EYETRACKER:
    pages.append(TPxReadingTrial(i,c,s,tpx))
  else:
    pages.append(ReadingTrial(i,c,s))
  if random.choice([True, False]):
    pages.append(YesNoQuestionTrial(i,c,q))
  pages.append(TPxNext(tpx))
pages.pop()


# Thank you screen:
pages.append(CenteredInstructions(" Done! Thank you very much for your participation."))

# Run experiment:
run_experiment(pages)
