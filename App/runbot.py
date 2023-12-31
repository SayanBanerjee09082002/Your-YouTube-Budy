from youtube_transcript_api import YouTubeTranscriptApi
import openai

openai.api_key = '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'
subtitle_text = ''

# to convert time from seconds into hour:mins:sec format
def seconds_to_hms(time_str):
  seconds = int(time_str)
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60
  return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# to call the youtube_transcript_api to get subtitles and store it in a global variable
def save_subtitles_to_file(video_url):
    global subtitle_text
    subtitle_text = ''
    try:
        video_id = video_url.split("v=")[1]
        subtitles = YouTubeTranscriptApi.get_transcript(video_id)
        for subtitle in subtitles:
            start_time = seconds_to_hms(subtitle['start'])
            end_time = seconds_to_hms(subtitle['duration'])
            subtitle_text+=f"{start_time} - {end_time}: {subtitle['text']} ;"
        print(subtitle_text)
        print('Printing')
        return subtitle_text
    except Exception as e:
        print(f"Error: {e}")
        return subtitle_text

#SUBTITLES
def getsubtitle(video_url):
    global subtitle_text
    subtitle_text = save_subtitles_to_file(video_url)
    print(subtitle_text)
    return subtitle_text

# to store previous messages in chat and generate answer to prompts on the basis of history of conversation
def get_completion_from_messages(messages, model="gpt-3.5-turbo-16k", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# to collect all the messages together and generate an array for conversations
def collect_messages(text,context):
    prompt = text
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({'role':'assistant', 'content':f"{response}"})
    return response

#ANSWER
def qna(question):
    context = [
      {'role':'system', 'content':f"""
      You are a youtube bot, a bot that answers questions from the subtitle file that you receive of the video.\
      You will get questions and you need to answer them according to the\
      the subtitles. If not present in it, then get then answer them accordingly but specify that.\
      You respond in a short, very conversational friendly style.\
      This is the subtitle of a youtube video: <{subtitle_text}>
      """}]
    answer=collect_messages(question,context)
    return answer
