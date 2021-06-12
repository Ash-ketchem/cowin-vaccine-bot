# cowin-vaccine-bot

a simple bot that polls for available vaccine slots and books them automatically on  India's Co-WIN Platform

This python script will poll for available vaccine slots in your given district/pincode and will automatically shedules vaccine appointment

 -----------------------------------------------------------


𝓕𝓮𝓪𝓽𝓾𝓻𝓮𝓼

$  𝘢𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤𝘢𝘭𝘭𝘺 𝘴𝘩𝘦𝘥𝘶𝘭𝘦𝘴 𝘢𝘱𝘱𝘰𝘯𝘪𝘵𝘮𝘦𝘯𝘵

$  𝘤𝘢𝘯 𝘣𝘰𝘰𝘬 𝘷𝘢𝘤𝘤𝘪𝘯𝘦𝘴 𝘧𝘰𝘳 𝘮𝘶𝘭𝘵𝘪𝘱𝘭𝘦 𝘱𝘦𝘳𝘴𝘰𝘯𝘴

$  𝘷𝘢𝘤𝘤𝘪𝘯𝘦 𝘴𝘭𝘰𝘵𝘴 𝘤𝘢𝘯 𝘣𝘦 𝘧𝘪𝘭𝘵𝘦𝘳𝘦𝘥 𝘣𝘺 𝘮𝘶𝘭𝘵𝘪𝘱𝘭𝘦 𝘥𝘢𝘵𝘦𝘴, 𝘷𝘢𝘤𝘤𝘪𝘯𝘦 𝘵𝘺𝘱𝘦𝘴, 𝘤𝘦𝘯𝘵𝘦𝘳𝘴, 𝘣𝘦𝘯𝘦𝘧𝘪𝘤𝘪𝘢𝘳𝘪𝘦𝘴, booking time

$  𝘴𝘶𝘱𝘱𝘰𝘳𝘵𝘴 𝘣𝘰𝘵𝘩 𝘥𝘰𝘴𝘦1 𝘢𝘯𝘥 𝘥𝘰𝘴𝘦2 𝘷𝘢𝘤𝘤𝘪𝘯𝘦 𝘣𝘰𝘰𝘬𝘪𝘯𝘨

$  𝘴𝘶𝘱𝘱𝘰𝘳𝘵𝘴 𝘷𝘢𝘤𝘤𝘪𝘯𝘦 𝘴𝘦𝘢𝘳𝘤𝘩 𝘣𝘺 𝘥𝘪𝘴𝘵𝘳𝘪𝘤𝘵 𝘰𝘳 𝘱𝘪𝘯𝘤𝘰𝘥𝘦

$ 𝘋𝘰𝘸𝘯𝘭𝘰𝘢𝘥𝘴 𝘢𝘱𝘱𝘰𝘪𝘯𝘵𝘮𝘦𝘯𝘵 𝘤𝘰𝘯𝘧𝘪𝘳𝘮𝘢𝘵𝘪𝘰𝘯 𝘱𝘥𝘧

$ 𝘔𝘢𝘹𝘪𝘮𝘶𝘮 𝘳𝘦𝘶𝘴𝘦 𝘰𝘧 𝘢𝘶𝘵𝘩 𝘵𝘰𝘬𝘦𝘯 

  
  -----------------------------------------------------------


𝓗𝓸𝔀 𝓽𝓱𝓲𝓼 𝔀𝓸𝓻𝓴𝓼  ?

1 . Polls cowin site for available vaccine slots according to your district or pincode.

2 . Shedules vaccine apponitment for all beneficiaries linked to the given mobile number at random centers with slot availabilty.  
     => T̳h̳a̳t̳'̳s̳ ̳n̳o̳t̳ ̳m̳u̳c̳h̳ ̳u̳s̳e̳f̳u̳l̳ 😒 🤦‍♂️

    To solve this issue a lot of filtering options are given to customize the search ::
    
    🎀 you can filter the slots by date ,vaccine type, booking time, beneficiaries and centers 😍
    
    🎀 you just have to google your area's latitude and longitude and feed it into the program,
        then you can select preferred centers  within 10 Km radius of your point of interest!!
        
3 . If no vaccine slots are available ,the script will poll for vaccine availabilty till everyone  linked to  the mobile number gets an appointment .

4 . Your last filters will be stored in a file and can be fed to the script, so that you don't have  to type everything again..

5 . This script will try to shedule appointment for people linked to a mobile number at the same    
    vaccine center if possible else it will balance out the sheduling process.
    
 
 
  ------------------------------------------------------------
 
  
 𝓗𝓸𝔀 𝓽𝓸 𝓾𝓼𝓮  ?
  
  𝔸ℙℙ𝕊
  
  1. install termux app from playstore 
  
  2. download and install termux api version 0.31 (older version) 
     https://apkpure.com/termux-api/com.termux.api/download/31-APK?from=versions%2Fversion
     
  𝕊𝔼𝕋𝕌ℙ   
  
  3 . clone this repo :  
  
         pkg install git && git clone https://github.com/Ash-ketchem/cowin-vaccine-bot.git
         
  4 . install requirements :
         cd to the path where you have cloned this repo
         
         bash install.sh
         
  5 . Run the script :
  
         python cowinbot.py -m mobile_num 
 
 
 
 
         
  𝓐𝓿𝓪𝓲𝓵𝓪𝓫𝓵𝓮 𝓪𝓻𝓰𝓾𝓶𝓮𝓷𝓽𝓼
  
     $  -𝘮  <𝘮𝘰𝘣𝘪𝘭𝘦 𝘯𝘶𝘮𝘣𝘦𝘳> required field  ✔
     
     $  -𝘥  <𝘥𝘰𝘴𝘦>  𝘥𝘦𝘧𝘢𝘶𝘭𝘵 𝘪𝘴 1 (𝘥𝘰𝘴𝘦 1)
     
     $  -𝘤  <𝘥𝘪𝘴𝘵𝘳𝘪𝘤𝘵 𝘪𝘥>  𝘥𝘦𝘢𝘧𝘶𝘭𝘵 𝘪𝘴 𝘬𝘰𝘵𝘵𝘢𝘺𝘢𝘮(301)
     
     $  -𝘰  <𝘰𝘵𝘱 𝘮𝘰𝘥𝘦>  𝘥𝘦𝘢𝘧𝘶𝘭𝘵 𝘪𝘴 𝘢𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤  [use '-o m' to manually provide otp ]
     
     $  --𝘱 <𝘱𝘪𝘯𝘤𝘰𝘥𝘦>
     
     $  -𝚝  <𝚋𝚘𝚘𝚔𝚒𝚗𝚐 𝚝𝚒𝚖𝚎>  𝚍𝚎𝚏𝚊𝚞𝚕𝚝 𝚒𝚜 𝟶 
          𝟶: "𝟶𝟿:𝟶𝟶𝙰𝙼-𝟷𝟷:𝟶𝟶𝙰𝙼"
          𝟷: "𝟷𝟷:𝟶𝟶𝙰𝙼-𝟶𝟷:𝟶𝟶𝙿𝙼"
          𝟸: "𝟶𝟷:𝟶𝟶𝙿𝙼-𝟶𝟹:𝟶𝟶𝙿𝙼"
          𝟹: "𝟶𝟹:𝟶𝟶𝙿𝙼-𝟶𝟼:𝟶𝟶𝙿𝙼"
          
     $  -𝘣  <𝘧𝘪𝘳𝘴𝘵 𝘯𝘢𝘮𝘦>  𝘤𝘢𝘯 𝘵𝘢𝘬𝘦 𝘢 𝘭𝘪𝘴𝘵 𝘰𝘧 𝘣𝘦𝘯𝘦𝘧𝘪𝘤𝘪𝘢𝘳𝘺 𝘯𝘢𝘮𝘦𝘴 𝘴𝘦𝘱𝘦𝘳𝘢𝘵𝘦𝘥 𝘣𝘺 𝘴𝘱𝘢𝘤𝘦
          
     $  --v  <vacccine type>  can take a list of vaccines seperated by space
     
     $  -𝘱  <𝘤𝘦𝘯𝘵𝘦𝘳 𝘪𝘥>  𝘤𝘢𝘯 𝘵𝘢𝘬𝘦 𝘢 𝘭𝘪𝘴𝘵 𝘰𝘧 𝘤𝘦𝘯𝘵𝘦𝘳 𝘪𝘥𝘴 𝘴𝘦𝘱𝘦𝘳𝘢𝘵𝘦𝘥 𝘣𝘺 𝘴𝘱𝘢𝘤𝘦
     
     $  --𝘥  <𝘥𝘢𝘵𝘦>  𝘤𝘢𝘯 𝘵𝘢𝘬𝘦 𝘢 𝘭𝘪𝘴𝘵 𝘰𝘧 𝘥𝘢𝘵𝘦𝘴  𝘴𝘦𝘱𝘦𝘳𝘢𝘵𝘦𝘥 𝘣𝘺 𝘴𝘱𝘢𝘤𝘦 (provide only day)
     
     $  -𝘷  𝘷𝘦𝘳𝘣𝘰𝘴𝘦 𝘰𝘶𝘵𝘱𝘶𝘵
     
     $ --𝚕  <𝚕𝚘𝚌𝚊𝚝𝚒𝚘𝚗> 𝚝𝚊𝚔𝚎𝚜 𝟺 𝚊𝚛𝚐𝚞𝚖𝚎𝚗𝚝𝚜 𝚜𝚝𝚊𝚝𝚎_𝚗𝚊𝚖𝚎 𝚍𝚒𝚜𝚝𝚛𝚒𝚌𝚝_𝚗𝚊𝚖𝚎 𝚕𝚊𝚝𝚒𝚝𝚞𝚍𝚎 𝚊𝚗𝚍 𝚕𝚘𝚗𝚐𝚒𝚝𝚞𝚍𝚎
     
     $  -𝘵  𝘵𝘦𝘴𝘵 𝘳𝘶𝘯 𝘧𝘰𝘳 𝘧𝘶𝘯!!
     
     $  -𝘧  𝘭𝘰𝘢𝘥𝘴 𝘱𝘳𝘦𝘷𝘪𝘰𝘶𝘴 𝘪𝘯𝘱𝘶𝘵 𝘥𝘢𝘵𝘢 𝘧𝘳𝘰𝘮 𝘢 𝘧𝘪𝘭𝘦
     
     
     
     
  𝓔𝔁𝓪𝓶𝓹𝓵𝓮 𝓾𝓼𝓪𝓰𝓮
     
     $  𝙥𝙮𝙩𝙝𝙤𝙣 𝙘𝙤𝙬𝙞𝙣𝙗𝙤𝙩.𝙥𝙮 -𝙢 123456789  [𝙗𝙖𝙨𝙞𝙘 𝙪𝙨𝙖𝙜𝙚]
     
     $  𝙥𝙮𝙩𝙝𝙤𝙣 𝙘𝙤𝙬𝙞𝙣𝙗𝙤𝙩.𝙥𝙮 -𝙢 123456789 -𝙙 2  -𝙘 151 -o m --p 686001
     
     $  𝙥𝙮𝙩𝙝𝙤𝙣 𝙘𝙤𝙬𝙞𝙣𝙗𝙤𝙩.𝙥𝙮 -𝙢 𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵 -𝙙 𝟮  -𝙘 𝟭𝟱𝟭  -𝗯  𝘀𝗮𝗺 𝗮𝗷𝗮𝘆  --𝘃  𝗰𝗼𝘄𝗮𝘅𝗶𝗻 𝗰𝗼𝘃𝗶𝘀𝗵𝗶𝗲𝗹𝗱  -𝘁 𝟭 --𝗱  𝟴 𝟭𝟬 𝟭𝟮
     
     $  𝙥𝙮𝙩𝙝𝙤𝙣 𝙘𝙤𝙬𝙞𝙣𝙗𝙤𝙩.𝙥𝙮 -𝙢 𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵   --𝗱 𝟴 -𝗯 𝘀𝗮𝗺 --𝗹 𝗸𝗲𝗿𝗮𝗹𝗮 𝗸𝗼𝘁𝘁𝗮𝘆𝗮𝗺 𝟵𝟭.𝟱𝟳 𝟭𝟳𝟱.𝟲𝟯
     
            --𝕝 𝕨𝕚𝕝𝕝 𝕡𝕣𝕠𝕧𝕚𝕕𝕖 𝕪𝕠𝕦 𝕨𝕚𝕥𝕙 𝕒 𝕝𝕚𝕤𝕥 𝕠𝕗 𝕔𝕖𝕟𝕥𝕖𝕣𝕤 𝕟𝕖𝕒𝕣 𝕪𝕠𝕦 𝕗𝕣𝕠𝕞 𝕨𝕙𝕚𝕔𝕙 𝕪𝕠𝕦 𝕔𝕒𝕟 𝕔𝕙𝕠𝕠𝕤𝕖 𝕡𝕣𝕖𝕗𝕖𝕣𝕖𝕕 𝕒𝕟𝕕 𝕒𝕝𝕤𝕠 𝕙𝕖𝕝𝕡𝕤 𝕥𝕠 𝕗𝕚𝕟𝕕 𝕕𝕚𝕤𝕥𝕣𝕚𝕔𝕥 𝕚𝕕 𝕠𝕗 𝕒 𝕕𝕚𝕤𝕣𝕥𝕚𝕔𝕥 [recommended option ✔✔ ]
             
     $  𝙥𝙮𝙩𝙝𝙤𝙣 𝙘𝙤𝙬𝙞𝙣𝙗𝙤𝙩.𝙥𝙮 -𝙛
     
             𝕦𝕤𝕖 -𝕗 𝕠𝕟 𝕤𝕖𝕔𝕠𝕟𝕕 𝕥𝕚𝕞𝕖 𝕥𝕠 𝕝𝕠𝕒𝕕 𝕡𝕣𝕖𝕧𝕚𝕠𝕦𝕤 𝕗𝕚𝕝𝕥𝕖𝕣𝕤
     
     
     
            
 
 
  -----------------------------------------------------------
   
   𝓜𝓸𝓻𝓮 𝓘𝓷𝓯𝓸..
   
      ! Termux api_v0.31 is used to automatically read otp message from the phone. The newer api dosen't allow message acesss 
   
      ! The minimum polling interval is set for 30 seconds
   
      ! A log file is written at log.txt with the date and time of script activity
  
    
    
    IMPORTANT
    __________
    
    $ This is a proof of concept project,so use at your own risk
    
         
   


   


