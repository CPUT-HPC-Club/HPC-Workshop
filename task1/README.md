# Task 1

The goal of this tutorial is to give you an understanding of how the network works and how to utilize the network to connect to a cluster.

Lets get a basic understanding of a local area network vs wide area network.

![image](/task1/img/lan_wan.jpg)

For the diagram above it should be clear that the LAN ip ranges and WAN ip ranges will differ. For a PC in LAN 1 to reach a PC in LAN 2, it will have to travel out of its local network and through some external network to reach LAN 2.

Always remember where you are and where your cluster is located.

## SSH

We will be using ssh to access our cluster. There are many different ssh tools. `Windows CLI` (command line interface) "cmd" , putty or MobaXterm.

![image](/task1/img/moba.jpg)

Highlighted above is all the most  important features we will use.

1. Start a new session
2. Select SSH
3. Enter the end point [remote host] ip
4. Enter the username
5. Locate and select the SSH private key

## SSH key

Your **first task** would be to create a new ssh key for your account. Be very careful with these steps as a mistake can lock you out of your account!

```bash
# Generate new ed25519 key
ssh-keygen -t ed25519 -C "your.email@example.com"

# navigate to ssh key folder
cd ~/.ssh

# Delete the old authorized list
rm authorized_keys

# Create a new empty list
touch authorized_keys

# Add new key to the authorized list of allowed keys
cat id_ed25519.pub >> authorized_keys
```

Make sure to `copy` the `id_ed25519` file to your local machine so that you can start using this as your new ssh key.

## Git

We will now setup and configure git. After git has been setup. Your **second task** is to clone the fork of the repo your captain has created. 

### Configure git

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Configure SSH for git

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Check if `SSH` is added to git config

```bash
ssh-add -l
```

### Add key to github

Print key

```bash
cat ~/.ssh/id_ed25519.pub
```

On `github` Select repo -> settings -> security -> deploy keys and paste ssh key

### Check SSH connection to Github

```bash
ssh -T git@github.com
```

If this hangs, try a [different port](#try-a-differnt-port) 

### Clone repo

```bash
git clone git@github.com:username/repo.git
```
---
### Try a differnt port

If you could not ssh test github, try a different port

```bash
ssh -T -p 443 git@ssh.github.com
```

If this works then :

```bash
vi ~/.ssh/config
```

Add the following:

```bash
Host github.com
  HostName ssh.github.com
  User git
  Port 443
  IdentityFile ~/.ssh/id_ed25519  
```

Press `esc` then type `:wq` and press enter

---

## Add moderators key

Your **third task** is to add the moderators ssh key to the authorized list of keys.

```bash
# Navigate to the key
cd hpc-workshop/task1/keys

# Copy the moderators key to the ssh key folder
cp <moderators_key> ~/.ssh/.

# Navigate to ssh folder
cd ~/.ssh

# add <moderators_key> to authorized list
```

## Final task

If you struggle with this task you can skip it as it wont stop you from completing the tutorials.

On the cluster machine:

1. Navigate to the app folder

```bash
cd ~/hpc-workshop/task1/app
```

2. Edit the `code.c` file and complete the **two** incomplete functions.

```bash
vim code.c
```

  - 1. Function to create a folder `void create_folder(char* name)`

  Complete this function so that it used the char* name variable to make a folder with that name.

  - 2. Function to create a file `void create_file(char* folder_name, char* group_name)`

  Complete this function so that it creates a file in the folder where the name will get passed to char* folder_name. Then add the string char* group_name to the file.

  - 3. Add a MakeFile to the app folder that has a make command to make the project, and a clean command to remove created files. The MakeFile should make object files as well as the project called app.

  Rules :

    - Do not edit the main.c or code.h files.

    - Use the function prototypes provided.

    - Commit and push to repo fork