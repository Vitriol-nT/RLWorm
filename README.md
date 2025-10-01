# Building Action Agent with Reinforcement Learning

Hello. This probably is going to be my biggest project ever.
DQN is applied based on modifying PyTorch DQN example code.
Displayed for my BIGDATA school club. Also, Classical DQN 
is not suitable for this kind of dynamic system. which is
hugely chaotic for it to handle.

## 1. Utilization

In order to use, run app.py and run it on your local host.
For your control, you will use W-A-S-D keys.
If your keyboard was switched to another language, it wouldn't work.
For example, if your keyboard is set to be Korean, resulting 'WASD' to be 'ㅈㅁㄴㅇ',
it wouldn't be able to read your controls.
Also, in order to use the DQN, you must pre-calculate the .pth file so that it could run without additional process.

For informations about DQN, please check other online informations.

---
## 2. Structure
**A2.py**: is a DQN model. For the current settings, it has 2 hidden layers with 128 neurons size. Using Adam for optimizing. For training, it performs 200k episodes which takes 200 steps each.
For current code, it has a kind of reward system and system which removes 10 steps after eating food at every episodes. Finally, the uploaded policy weights map will be the one calculated without that logic.
1. **Loss Function**: Mean Absolute Error function (L1loss)
2. **Gradient Descent**: Adam
3. **Memory Buffer**: 1 mil
4. **Neural Networks**: (If not modified) contains 4 layers. Input layer as n.observations which is 400, 2 hidden layers with each 128 neurons, and output layer with n.actions which is 4. Consisting one with 68356 parameters.


**Module.py** if you checked the file histories, you'll know that suddenly the head is changed to 3. This is because not only you cannot tell whether the part is head or tail, but also I found out that DQN cannot also be able to tell which is head to tail since it all defined worm as 1. Also, since the original logic of body collison made error of "List out of index" and other sorts of reasons, the logic on here changed little bit too.



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

**Trained AI (It prioritizes longevity😅)**

[
https://github.com/Vitriol-nT/RLWorm/issues/2#issue-3460670478
](https://github.com/user-attachments/assets/a52f0a51-cec7-4116-8a98-54ca4655e70c
)
