
# Create pictures folder and link if not exists yet.
FileUtils.mkdir_p("/var/www/akimoto/pictures")
FileUtils.ln_s("/var/www/akimoto/pictures", "/var/www/akimoto/current/public/pictures", :force => true)