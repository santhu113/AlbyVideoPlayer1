
<p align="center">
  <img src="https://te.legra.ph/file/965b2df3eeaf45cc5a291.jpg"</p>






echo "Cloning Repo...."
if [ -z $BRANCH ]
then
  echo "Cloning main branch...."
  git clone https://github.com/albinpraveen/AlbyVideoPlayer /AlbyVideoPlayer
else
  echo "Cloning $BRANCH branch...."
  git clone https://github.com/hackerkerala/VCPlayerBot -b $BRANCH /AlbyVideoPlayer
fi
cd /AlbyVideoPlayer
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 main.py
