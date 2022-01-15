#! /bin/bash

DIR="/Users/chenwen/Documents/Github"

git_repo="my_sre_story my_sre_story_private Demographic-Prediction-Based-on-Scikit-learn local_repo_for_rhel-centos"

echo -e "Pulling from github.com...\033[80G\033[5;32mSyncing\033[0m"

num=1
for repo in $(echo ${git_repo}); do

    cd $DIR/${repo}

    branch_name=$(git branch | head -n 1 | awk '{print $NF}')

    echo -e -n "Pull ${num}. ${repo}:origin/${branch_name}\033[80G\033[5;33mSyncing\033[0m"
    git pull origin ${branch_name} &>/dev/null
    [ $? -eq 0 ] && status="32m[OK]" || status="31m[ERROR]"
    echo -e "\033[7D\033[K\033[${status}\033[0m"

    let num+=1
done
echo -e "\033[5A\033[80G\033[K\033[32m[Completed!]\033[0m\033[4B"