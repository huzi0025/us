import os

# 📁 Path to the folder containing all HTML and CSS files (including subfolders)
folder_path = r"D:\hi old web"

# GTM script to insert in <head>
html_script_tag = '''<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-W29VHND9');</script>
<!-- End Google Tag Manager -->'''

# GTM noscript to insert after <body>
html_noscript_tag = '''<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-W29VHND9"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->'''

# CSS rule to add at top of .css files
css_line_to_add = '''* {
    background-color: #d1dceb !important;
}
'''

# Process all HTML and CSS files in directory tree
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)

        # 💡 Handle HTML Files
        if file.endswith(".html"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.readlines()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.readlines()

            # Remove previous copies of the script and noscript blocks
            cleaned_content = []
            for line in content:
                if (html_script_tag.strip() not in line.strip() and
                    html_noscript_tag.strip() not in line.strip()):
                    cleaned_content.append(line)

            # Insert script after <head>
            final_content = []
            script_inserted = False
            noscript_inserted = False
            for line in cleaned_content:
                final_content.append(line)
                if not script_inserted and '<head>' in line.lower():
                    final_content.append(html_script_tag + "\n")
                    script_inserted = True
                if not noscript_inserted and '<body>' in line.lower():
                    final_content.append(html_noscript_tag + "\n")
                    noscript_inserted = True

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(final_content)

        # 💡 Handle CSS Files
        elif file.endswith(".css"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    css_content = f.read()

            # Add CSS rule at top if not already present
            if css_line_to_add.strip() not in css_content:
                new_css_content = css_line_to_add + "\n" + css_content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_css_content)

print("✅ Done: GTM script added after <head>, GTM noscript added after <body>, CSS rule added at top.")
