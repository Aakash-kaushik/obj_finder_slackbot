import os
import time
import re
from slackclient import SlackClient
from mmdet.apis import init_detector, inference_detector, show_result
import mmcv
import cv2
import numpy as np

config_file = 'configs/faster_rcnn_r50_fpn_1x.py'
checkpoint_file = '/home/aakash/.cache/torch/checkpoints/faster_rcnn_r50_fpn_1x_20181010-3d1b3351.pth'

model = init_detector(config_file, checkpoint_file, device='cuda:0')

token="xoxb-965578669089-985477691573-PGSsnA3lVorBie2AkCY9zafK"
# instantiate Slack client
slack_client = SlackClient(token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

items=['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine_glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Can't do that yet"
    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command not in items:
        response = "I can't find that yet"
    if command.startswith("lost"):
        response = "Sure let me help you find it, mention me again and type what's lost"
    if command in items:
        search_item=command
        idx=items.index(search_item)
        slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text="give me a moment......"
        )
        cap=cv2.VideoCapture(0)
        ret,frame=cap.read()
        result = inference_detector(model, frame)
        num_res=np.array(result[idx])
        num_res=num_res[num_res[:,4]>0.325]
        response="I found "+str(num_res.shape[0])+" "+search_item+"."
        slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text="here are the pictures of what i found."
        )
        img=np.array(frame)
        num_res=num_res.astype(int)
        for img_idx in range(num_res.shape[0]):
          crop=img[num_res[img_idx,1]:num_res[img_idx,3],num_res[img_idx,0]:num_res[img_idx,2]]
          cv2.imwrite("obj.png",crop)
          slack_client.api_call(
          "files.upload",
           channels=[channel],
           file=open('obj.png','rb')
           )
    
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")





