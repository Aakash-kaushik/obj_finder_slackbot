# object Finder Slack Bot
It is a slack bot that can find your lost objects, you can deploy this for your workspace and help others in finding their lost objects.
This project used [mmdetection](https://github.com/open-mmlab/mmdetection).
### Team Members
* [Aakash Kaushik](https://github.com/Aakash-kaushik)
* [Kunal Mundada](https://github.com/AlKun25)
* [Satyam Sai](https://github.com/Satyamsai)
### guide to use 
* You first need to install mmdetection, instructions are given [here](https://github.com/open-mmlab/mmdetection/blob/master/docs/INSTALL.md)
* you need to download the model and choose the config file accoridng to the model you wish to use from the mmdetection model.
* We used the cascade_rcnn_x101_64x4d_fpn_1x pre trained model.
* then move the contents of this repo to the mmdetection directory that you cloned and change the variables in the slack_bot.py file accordingly to access the model and config file from mmdetection you wish to use.
* the slack_bot.py file contains the basic command you can add according to your use and requires a bot token before you can start using it.
* dark_img_tool.py contains tools to detect dark image and to enhacne we weren't able to make the dark image detector functions work.
### Contributions
 We appreciate all Contributions and there are no hard and strict rules for the contribution just try to keep things organised while working.
