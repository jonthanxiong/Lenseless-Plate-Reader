import os

#Place files to be reformatted in same directory as this python file.

xml_files = []

for _,_,files in os.walk("."):
    for file in files:
        if file.endswith(".xml"):
            xml_files.append(file)
    break

for file in xml_files:
    lines = None
    with open(file) as f:
        lines = f.read().splitlines()
    with open("reformated/" + file, "w") as f:
        f.write("<annotation>\n")
        f.write("\t<filename>"+file.split(".")[0] + ".jpg"+"</filename>\n")
        f.write("\t<folder>cells</folder>\n")
        f.write("\t<source>\n")
        f.write("\t\t<database>cells</database>\n")
        f.write("\t\t<annotation>custom</annotation>\n")
        f.write("\t\t<image>custom</image>\n")
        f.write("\t</source>\n")

        found = 0
        for line in lines:
            if found == 4:
                f.write(line+"\n")
                break
            if found > 0 and found < 4:
                found+=1
                f.write(line+"\n")
            if "<size>" in line:
                found = 1
                f.write(line+"\n")

        f.write("\t<segmented>0</segmented>\n")

        found = False
        for line in lines:
            if not found and "<object>" in line:
                found = True
            if found:
                if "<pose>" in line:
                    f.write(line.split("Unspecified")[0] + "unspecified" + line.split("Unspecified")[1]+"\n")
                elif "<truncated>" in line or "<difficult>" in line:
                    f.write(line.split("Unspecified")[0] + "0" + line.split("Unspecified")[1]+"\n")
                elif "</annotation>" in line:
                    f.write(line)
                else:
                    f.write(line+"\n")
