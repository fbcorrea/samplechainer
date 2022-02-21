from flask import Flask
from flask import render_template, request, redirect, Response
from pydub import AudioSegment
import glob
import numpy
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload():
	# defining arrays
	sound_array = []
	sound_length_array = []

	if request.method == "POST":
		if request.files:
			
			uploaded_files = request.files.getlist("file[]")
			
			#print(uploaded_files)
			# Check if there is no WAV file
			for wav_file in uploaded_files:
				if wav_file.content_type != "audio/x-wav":
					print("File type not supported!")
					#break
					return redirect(request.url)
				else:
					# load file as audiosegment object
					sound = AudioSegment.from_wav(wav_file)
					# append to array
					sound_array.append(sound)
					sound_length_array.append(sound.duration_seconds)
					# test printing attributes
					#print(sound.duration_seconds)
			
			# collect maximum duration of a sound
			max_duration = numpy.max(sound_length_array)

			# append silence to make all sounds the same length
			for index in range(len(sound_array)):

				silence_to_append = max_duration - sound_array[index].duration_seconds

				#print(sound_array[index].duration_seconds * 1000, silence_to_append, max_duration, silence_to_append + sound_array[index].duration_seconds)
				sound_array[index] = sound_array[index] + AudioSegment.silent(duration=silence_to_append*1000, frame_rate=44100)

			#iterate and append audio to final clip
			final_clip = sound_array[0]

			for index in range(1,len(sound_array)):

				#print(sound_array[index].duration_seconds)
				final_clip = final_clip + sound_array[index]

			#print(final_clip)
			final_clip_wav = final_clip.export(format="wav")

			unique_filename = str(uuid.uuid4().hex)
			print(unique_filename)
			#file_test=(str.join('', ('"Content-Disposition":"attachment;filename=',unique_filename,'.wav"')))
			return Response(final_clip_wav, mimetype="audio/x-wav",
				headers={"Content-Disposition":"attachment;filename=test.wav"})
				#headers={file_test})
				
			return redirect(request.url)

	return render_template("upload.html")


if __name__ == '__main__':

	app.run()