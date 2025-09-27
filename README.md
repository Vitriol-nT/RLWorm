# Building Action Agent with Reinforcement Learning

Hello. This probably is going to be my biggest project ever.
DQN is applied based on modifying PyTorch DQN example code.

## 1. Utilization

In order to use, run app.py and run it on your local host.
For your control, you will use W-A-S-D keys.
If you're keyboard was switched to another language, it wouldn't work.
For example, if your keyboard is set to be Korean, resulting 'WASD' to be 'ㅈㅁㄴㅇ',
it wouldn't be able to read your controls.
Also, in order to use the DQN, you must pre-calculate the .pth file so that it could run without additional process.

---
## 2. Structure
**A2**: is a DQL model. For the current settings, it has 2 hidden layers with 128 neurons size. Using Adam for optimizing. For training, it performs 500 episodes which takes 300 steps each.
For current code, it has a kind of reward system which adds 10 steps after eating food at every episodes. It will probably good for improvements, but definitely will take longer
to process. So, the uploaded policy weights map will be the one calculated without that logic.


---


## 3. Comments
**1.** The movement of AI will be following after your move. Which is live-action.

**2.** The game will start as soon as you start giving the application a input.

---
## 4. Gallery

**User Input**

[
https://github.com/Vitriol-nT/RLWorm/issues/1#issue-3421098382
](https://github.com/user-attachments/assets/df496e81-3725-4d37-a77f-83bd036c6483
)

**Training**
<img width="1512" height="982" alt="Screenshot 2025-09-27 at 11 30 27 AM" src="https://github.com/user-attachments/assets/f1de3a38-65e2-4017-8631-5fd7d7fe41ac" />
