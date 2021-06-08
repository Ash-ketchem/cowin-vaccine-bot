# cowin-vaccine-bot

a simple bot that polls for available vaccine slots and books them automatically on  India's Co-WIN Platform

This python script will poll for available vaccine slots in your given district/pincode and will automatically shedules vaccine appointment


🅵🅴🅰🆃🆄🆁🅴🆂

$  𝘢𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤𝘢𝘭𝘭𝘺 𝘴𝘩𝘦𝘥𝘶𝘭𝘦𝘴 𝘢𝘱𝘱𝘰𝘯𝘪𝘵𝘮𝘦𝘯𝘵

$  𝘤𝘢𝘯 𝘣𝘰𝘰𝘬 𝘷𝘢𝘤𝘤𝘪𝘯𝘦𝘴 𝘧𝘰𝘳 𝘮𝘶𝘭𝘵𝘪𝘱𝘭𝘦 𝘱𝘦𝘳𝘴𝘰𝘯𝘴

$  𝘷𝘢𝘤𝘤𝘪𝘯𝘦 𝘴𝘭𝘰𝘵𝘴 𝘤𝘢𝘯 𝘣𝘦 𝘧𝘪𝘭𝘵𝘦𝘳𝘦𝘥 𝘣𝘺 𝘮𝘶𝘭𝘵𝘪𝘱𝘭𝘦 𝘥𝘢𝘵𝘦𝘴, 𝘷𝘢𝘤𝘤𝘪𝘯𝘦 𝘵𝘺𝘱𝘦𝘴, 𝘤𝘦𝘯𝘵𝘦𝘳𝘴, 𝘣𝘦𝘯𝘦𝘧𝘪𝘤𝘪𝘢𝘳𝘪𝘦𝘴, booking time

$  𝘴𝘶𝘱𝘱𝘰𝘳𝘵𝘴 𝘣𝘰𝘵𝘩 𝘥𝘰𝘴𝘦1 𝘢𝘯𝘥 𝘥𝘰𝘴𝘦2 𝘷𝘢𝘤𝘤𝘪𝘯𝘦 𝘣𝘰𝘰𝘬𝘪𝘯𝘨

$  𝘴𝘶𝘱𝘱𝘰𝘳𝘵𝘴 𝘷𝘢𝘤𝘤𝘪𝘯𝘦 𝘴𝘦𝘢𝘳𝘤𝘩 𝘣𝘺 𝘥𝘪𝘴𝘵𝘳𝘪𝘤𝘵 𝘰𝘳 𝘱𝘪𝘯𝘤𝘰𝘥𝘦


🅷🅾🆆 🆃🅷🅸🆂 🆆🅾🆁🅺🆂 ?

1 . Polls cowin site for available vaccine slots according to your district or pincode

2 . Shedules vaccine apponitment for all beneficiaries linked to the given mobile number at random       centers with slot availabilty.  🆃🅷🅰🆃🆂 🅽🅾🆃 🅼🆄🅲🅷 🆄🆂🅴🅵🆄🅻🅻 😒 

    To solve this issue a lot of filtering options are given to customize the search ::
    
    🎀 you can filter the slots by date ,vaccine type, booking time and centers 😍
    
    🎀 you just have to google your area's latitude and longitude and feed it into the program,
        then you can select preferred centers  within 10 Km radius of your point of interest!!
        
3 . If no vaccine slots are available ,the script will poll for vaccine availabilty till everyone         linked to  the mobile number gets an appointment 

4 . Your last filters will be stored in a file and can be fed to the script, so that you don't have       to type everything again..

5 . This script will try to shedule appointment for people linked to a mobile number at the same    
    vaccine center if possible else it will balance out the sheduling process
    
  
  🅷🅾🆆 🆃🅾 🆄🆂🅴 ?
  
  𝔸ℙℙ𝕊
  
  1. install termux app from playstore 
  
  2. download and install termux api version 0.31 (older version) 
     https://apkpure.com/termux-api/com.termux.api/download/31-APK?from=versions%2Fversion
     
  
  3 . clone this repo :  
  
         pkg install git && git clone this repo
         
  4 . install requirements :
         cd to the path where you have cloned this repo
         
         bash install.sh
         
  5 . Run the script :
  
         python cowinbot.py -m mobile_num 
         
         
  🅰🆅🅰🅸🅻🅰🅱🅻🅴 🅰🆁🅶🆄🅼🅴🅽🆃🆂 
  
     $  -𝘮 <𝘮𝘰𝘣𝘪𝘭𝘦 𝘯𝘶𝘮𝘣𝘦𝘳> required field  ✔
     
     $  -𝘥 <𝘥𝘰𝘴𝘦>  𝘥𝘦𝘧𝘢𝘶𝘭𝘵 𝘪𝘴 1 (𝘥𝘰𝘴𝘦 1)
     
     $  -𝘤 <𝘥𝘪𝘴𝘵𝘳𝘪𝘤𝘵 𝘪𝘥>  𝘥𝘦𝘢𝘧𝘶𝘭𝘵 𝘪𝘴 𝘬𝘰𝘵𝘵𝘢𝘺𝘢𝘮(301)
     
     $  -𝘰 <𝘰𝘵𝘱 𝘮𝘰𝘥𝘦>  𝘥𝘦𝘢𝘧𝘶𝘭𝘵 𝘪𝘴 𝘢𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤
     
     $  -𝚝 <𝚋𝚘𝚘𝚔𝚒𝚗𝚐 𝚝𝚒𝚖𝚎>  𝚍𝚎𝚏𝚊𝚞𝚕𝚝 𝚒𝚜 𝟶 
          𝟶: "𝟶𝟿:𝟶𝟶𝙰𝙼-𝟷𝟷:𝟶𝟶𝙰𝙼"
          𝟷: "𝟷𝟷:𝟶𝟶𝙰𝙼-𝟶𝟷:𝟶𝟶𝙿𝙼"
          𝟸: "𝟶𝟷:𝟶𝟶𝙿𝙼-𝟶𝟹:𝟶𝟶𝙿𝙼"
          𝟹: "𝟶𝟹:𝟶𝟶𝙿𝙼-𝟶𝟼:𝟶𝟶𝙿𝙼"
          
     $  --v <vacccine type>  can take a list of vaccines seperated by space
     
     $  -𝘱 <𝘤𝘦𝘯𝘵𝘦𝘳 𝘪𝘥>  𝘤𝘢𝘯 𝘵𝘢𝘬𝘦 𝘢 𝘭𝘪𝘴𝘵 𝘰𝘧 𝘤𝘦𝘯𝘵𝘦𝘳 𝘪𝘥𝘴 𝘴𝘦𝘱𝘦𝘳𝘢𝘵𝘦𝘥 𝘣𝘺 𝘴𝘱𝘢𝘤𝘦
     
     $  --𝘥 <𝘥𝘢𝘵𝘦>  𝘤𝘢𝘯 𝘵𝘢𝘬𝘦 𝘢 𝘭𝘪𝘴𝘵 𝘰𝘧 𝘥𝘢𝘵𝘦𝘴  𝘴𝘦𝘱𝘦𝘳𝘢𝘵𝘦𝘥 𝘣𝘺 𝘴𝘱𝘢𝘤𝘦
     
     $  -𝘷 <𝘷𝘦𝘳𝘣𝘰𝘴𝘦 𝘮𝘰𝘥𝘦>  𝘷𝘦𝘳𝘣𝘰𝘴𝘦 𝘰𝘶𝘵𝘱𝘶𝘵
     
     $ --𝚕 <𝚕𝚘𝚌𝚊𝚝𝚒𝚘𝚗> 𝚝𝚊𝚔𝚎𝚜 𝟺 𝚊𝚛𝚐𝚞𝚖𝚎𝚗𝚝𝚜 𝚜𝚝𝚊𝚝𝚎_𝚗𝚊𝚖𝚎 𝚍𝚒𝚜𝚝𝚛𝚒𝚌𝚝_𝚗𝚊𝚖𝚎 𝚕𝚊𝚝𝚒𝚝𝚞𝚍𝚎 𝚊𝚗𝚍 𝚕𝚘𝚗𝚐𝚒𝚝𝚞𝚍𝚎
     
     $  -𝘵 <𝘵𝘦𝘴𝘵 𝘳𝘶𝘯> 𝘧𝘰𝘳 𝘧𝘶𝘯!!
     
     
  
    
    
    
         
   


   


