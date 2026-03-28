import os
import glob

def main():
    sd_group = os.environ.get('SD_GROUP')
    if not sd_group:
        print("Warning: SD_GROUP environment variable is not set. Using default 'china'")
        sd_group = 'china'

    current_directory = os.getcwd()
    converted_directory = os.path.join(current_directory, 'converted')
    os.makedirs(converted_directory, exist_ok=True)

    conf_files = glob.glob(os.path.join(current_directory, '*china.conf'))
    output_file = os.path.join(converted_directory, 'chinadomain.conf')

    print(f"Generating {output_file}...")

    with open(output_file, 'w') as out:
        for thefile in conf_files:
            filename = os.path.basename(thefile)
            if filename == 'bogus-nxdomain.china.conf':
                continue
            
            target_group = sd_group
            if filename == 'apple.china.conf':
                target_group = 'apple'
            elif filename == 'google.china.conf':
                target_group = 'google'

            print(f"Processing {filename}...")
            with open(thefile, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    parts = line.split('=')
                    if len(parts) != 2:
                        continue
                    
                    # expected format: server=/domain/dns_ip
                    # parts[1] should be /domain/dns_ip
                    val_parts = parts[1].split('/')
                    if len(val_parts) >= 2:
                        domain = val_parts[1]
                        if domain:
                            out.write(f"nameserver /{domain}/{target_group}\n")

    print("Done.")

if __name__ == "__main__":
    main()
