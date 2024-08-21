set user name to same as on server 


```.env
myusername=marc.keeling
```

the llm_prep file is used to concatenate files together to feed into an LLM to get help modifying things. 


helps to start an ssh agent on the image so you don't have to enter in your key all the time
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa 
```

command to install extensions
```bash
code --install-extension extensions.txt
```