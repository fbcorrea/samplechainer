from flask import Flask
from flask import render_template, request, redirect, make_response, flash
from pydub import AudioSegment
import glob
import numpy
import os
import uuid

app = Flask(__name__)
app.secret_key = "secret_key_samplechain"

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
			# if len(uploaded_files) == 1:
			# 	flash('Please provide more than one file!', category='error')
			# 	return redirect(request.url)

			for wav_file in uploaded_files:
				if wav_file.content_type not in ("audio/x-wav", "audio/wav"):
					print(wav_file.content_type)
					flash('File type not supported!', category='error')
					return redirect(request.url)
				elif len(uploaded_files) == 1:
					flash('Please provide more than one file!', category='error')
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

			# return final clip to client
			final_clip_wav = final_clip.export(format="wav")

			unique_filename = str(uuid.uuid4().hex)
			print(unique_filename)
			number_of_hits = str(len(sound_array))

			response = make_response(final_clip_wav.read())
			response.headers.set('Content-Type', 'audio/x-wav')
			response.headers.set('Content-Disposition', 'attachment', 
				filename=unique_filename+"_"+number_of_hits)
			
			return response
			#return redirect(request.url)

			#flash('File(s) successfully uploaded')
			#return redirect(url_for('update'))
			#return redirect('/')

	return render_template("upload.html")


if __name__ == '__main__':

	app.run(host='0.0.0.0', port=5000)