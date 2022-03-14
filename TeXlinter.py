#!/usr/bin/env python3

import sys
import json
import yaml
import time
import pathlib
import platform
import argparse

def tex_Linter(user_input, rules, header = False):
    index = user_input.find('.')
    indent_bool = False
    indent_begining_rules, indent_ending_rules, comment_rules, exclude_rules, newline_rules, configureable_rules, newlines_before = get_rules(rules)
    newline_counter = configureable_rules[0]
    newline_bool = configureable_rules[1]
    newline_bool_counter = 0
    ext = user_input.rpartition('.')[-1]
    if header == True:
        used_indent = False
        used_newlines = False
        used_comments = False
    with open(user_input, "r") as infile, open("Validated_file." + ext, "w+") as outfile:
        for line in infile:
            if any(rule in line for rule in exclude_rules):
                if any(rule in line for rule in comment_rules):
                    if len(line.split()) != 1:
                        first_word, *middle_words, last_word = line.split()
                        if not any(rule in first_word for rule in exclude_rules):
                            outfile.write('\t')
                        for word in line.split():
                            for comment in comment_rules:
                                # Checks if the words contains any comments and does not have a lenght of 1
                                if word.__contains__(comment):
                                    used_comments = True
                                    # Gets the index of where the comment is
                                    comment_index = word.find(comment)
                                    # If the comment does not have a \ in it oterwise it just writes the word to the file
                                    if not any(rule in word[:comment_index] for rule in exclude_rules):
                                        outfile.write(word[:comment_index] + ' ' + word[comment_index] + ' ' + word[comment_index + 1:] + ' ')
                                    else:
                                        if any(rule in word[:comment_index + 1] for rule in exclude_rules):
                                            try:
                                                if any(rule in word[:comment_index + 2] for rule in comment_rules):
                                                    if indent_bool == True and word == first_word:
                                                        outfile.write('\t' * newline_bool_counter + word[:comment_index + 1] + ' ' + word[comment_index + 1] + ' ' + word[comment_index + 2:] + ' ')
                                                    elif any(rule in word[comment_index + 1] for rule in comment_rules):
                                                        outfile.write(word[:comment_index + 1] + ' ' + word[comment_index + 1] + ' ' + word[comment_index + 2:] + ' ')
                                                    elif any(rule in word[comment_index + 1] for rule in newline_rules):
                                                        if newline_bool == True:
                                                            outfile.write('\t' * (newline_bool_counter - 1))
                                                            outfile.write(word + '\n')
                                                            outfile.write('\t' * newline_bool_counter)
                                                        else:
                                                            outfile.write(word + ' ')
                                                    else:
                                                        outfile.write(word + ' ')
                                                else:
                                                    outfile.write(word + ' ')
                                            except IndexError:
                                                outfile.write(word + ' ')
                                else:
                                    # Checks if there is a newline_rules in the word
                                    if newline_bool == True:
                                        used_indent = True
                                        if any(rule in word for rule in indent_begining_rules):
                                            newline_bool_counter += 1
                                            indent_bool = True
                                        elif any(rule in word for rule in indent_ending_rules):
                                            newline_bool_counter -= 1
                                            indent_bool = False
                                        if any(rule in word for rule in newline_rules):
                                            used_newlines = True
                                            if word == first_word:
                                                outfile.write('\t' * (newline_bool_counter - 1))
                                                outfile.write(word + '\n')
                                                outfile.write('\t' * newline_bool_counter)
                                            else:
                                                outfile.write(word + '\n')
                                                outfile.write('\t' * newline_bool_counter)
                                        else:
                                            outfile.write(word + ' ')
                                    else:
                                        outfile.write(word + ' ')
                            if word == last_word:
                                outfile.write('\n')
                    else:
                        # Fixes comments that is in the indent rules
                        if any(rule in line for rule in comment_rules):
                            used_comments = True
                            if any(rule in line for rule in indent_begining_rules):
                                for comment in comment_rules:
                                    comment_index = line.find(comment)
                                    if not line.startswith(comment):
                                        if indent_bool == True:
                                            outfile.write('\t' * newline_bool_counter)
                                            outfile.write(line[:comment_index] + ' ' + line[comment_index] + ' ' + line[comment_index + 1:] + ' ')
                                            newline_bool_counter += 1
                                        else:
                                            outfile.write(line[:comment_index] + ' ' + line[comment_index] + ' ' + line[comment_index + 1:] + ' ')
                                            newline_bool_counter += 1
                                        indent_bool = True
                                    else:
                                        if indent_bool == True:
                                            outfile.write('\t' * newline_bool_counter)
                                            outfile.write(line[:comment_index] + ' ' + line[comment_index] + ' ' + line[comment_index + 1:] + ' ')
                                        else:
                                            outfile.write(line[:comment_index] + ' ' + line[comment_index] + ' ' + line[comment_index + 1:] + ' ')
                            elif any(rule in line for rule in indent_ending_rules):
                                used_indent = True
                                if newline_bool_counter <= 0:
                                    newline_bool_counter = 1
                                for comment in comment_rules:
                                    comment_index = line.find(comment)
                                    if not line.startswith(comment):
                                        if indent_bool == True:
                                            outfile.write('\t' * newline_bool_counter)
                                            outfile.write(line[:comment_index] + ' ' + line[comment_index] + ' ' + line[comment_index + 1:] + ' ')
                                            newline_bool_counter -= 1
                                        else:
                                            outfile.write(line[:comment_index] + ' ' + line[comment_index] + ' ' + line[comment_index + 1:] + ' ')
                                            newline_bool_counter -= 1
                                        indent_bool = False
                                    else:
                                        if indent_bool == True:
                                            outfile.write('\t' * newline_bool_counter)
                                            outfile.write(line[:comment_index] + ' ' + line[comment_index] + ' ' + line[comment_index + 1:] + ' ')
                                        else:
                                            outfile.write(line[:comment_index] + ' ' + line[comment_index] + ' ' + line[comment_index + 1:] + ' ')
                            else:
                                for comment in comment_rules:
                                    comment_index = line.find(comment)
                                    outfile.write('\t' * newline_bool_counter)
                                    outfile.write(line[:comment_index] + ' ' + line[comment_index] + ' ' + line[comment_index + 1:] + ' ')
                                    
                # This will add indenting to everything that is between \begin and \end that is not ordinary text
                elif any(rule in line for rule in indent_begining_rules) and not any(rule in line for rule in comment_rules):
                    used_indent = True
                    if indent_bool == True:
                        outfile.write(newline_bool_counter * '\t' + line)
                        newline_bool_counter += 1
                    else:
                        outfile.write('\n' + line)
                        newline_bool_counter += 1
                    indent_bool = True
                elif any(rule in line for rule in indent_ending_rules):
                    if newline_bool_counter <= 0:
                        newline_bool_counter = 1
                    if indent_bool == True:
                        newline_bool_counter -= 1
                        outfile.write(newline_bool_counter * '\t' + line)
                    else:
                        newline_bool_counter -= 1
                        outfile.write(newline_bool_counter * '\t' + line)
                        
                    indent_bool = False
                elif indent_bool == True:
                    if any(rule in line for rule in newlines_before):
                        outfile.write('\n' * newline_counter +  '\t' * newline_bool_counter + line)
                else:
                    
                    outfile.write(line + '\n')
            else:
                # This is where te ordinary text is handeld
                if line != '\n' and indent_bool == True:
                    if not len(line.split()) == 1:
                        first, *middle, last = line.split()
                        # Adds the first word of each sentence to the file
                        if not any(rule in first for rule in newline_rules):
                            outfile.write('\t' * newline_bool_counter + first + ' ')
                        else:
                            outfile.write('\t' * newline_bool_counter + first + ' ')
                        if newline_bool == True:
                            for word in middle:
                                # This checks if the words inbetween the first and last word does not have any comments in them 
                                # and if they have any newline_rules
                                if any(rule in word for rule in newline_rules) and not any(rule in line for rule in comment_rules):
                                    # If they do have, it will add the words unitill any rule in newline_rules gets find it will add a newline after.
                                    used_newlines = True
                                    for newline in newline_rules:
                                        if word.count(newline) <= 1:
                                            outfile.write(word + '\n')
                                            outfile.write('\t' * newline_bool_counter)
                                        else:
                                            outfile.write(word + ' ')
                                # Checks if the sentence does not have any newline_rules and or comments in them
                                elif not any(rule in line for rule in comment_rules) and not any(rule in line for rule in newline_rules):
                                    outfile.write(word + ' ')
                                else:
                                    # If the word does have a newline_rules and a comment_rules in them
                                    if any(rule in word for rule in newline_rules) and any(rule in line for rule in comment_rules):
                                        used_comments = True
                                        used_newlines = True
                                        for comment in comment_rules:
                                            for newline in newline_rules:
                                                # Checks if the words contains any comments and does not have a lenght of 1
                                                if word.count(newline) <= 1 and line.__contains__(comment):
                                                    comment_index = word.find(comment)
                                                    new_comment_index = line.find(comment)
                                                    if word[comment_index] == comment:
                                                        outfile.write(word[:comment_index] + ' ' + word[comment_index] + ' ' + word[comment_index + 1:] + ' ')
                                                    elif word not in line[new_comment_index + 1:]:
                                                        outfile.write(word + '\n' + '\t' * newline_bool_counter)
                                                    else:
                                                        outfile.write(word + ' ')
                                                else:
                                                    outfile.write(word + ' ')
                                    # If the word does have a newline_rules and not a comment_rules in them
                                    elif not any(rule in word for rule in comment_rules):
                                        outfile.write(word + ' ')
                                    elif len(word) == 1:
                                        outfile.write(word + ' ')
                        outfile.write(last + '\n')
                    else:
                        outfile.write('\t' * newline_bool_counter + line)
                elif line != '\n':
                    outfile.write(line)
                else:
                    outfile.write(line)
    if header == True:
        if used_comments == True:
            print(" * Comments have been seperated")
        if used_indent == True:
            print(" * Text have been indented accordingly")
        if used_newlines == True:
            print(" * New lines have been applied")
            print('\n')


# Gets the rules from the config file and puts them in different lists
def get_rules(rules):
    indent_begining_rules = []
    indent_ending_rules = []
    comment_rules = []
    exclude_rules = []
    newline_rules = []
    configureable_rules = []
    newlines_before = []
    for data in rules:
        for rule in rules[data]:
            if data == "comment_rules":
                comment_rules.append(rules[data][rule])
            elif data == "indented_begining_rules":
                indent_begining_rules.append(rules[data][rule])
            elif data == "indented_ending_rules":
                indent_ending_rules.append(rules[data][rule])
            elif data == "exlude_rules":
                exclude_rules.append(rules[data][rule])
            elif data == "newline_rules":
                newline_rules.append(rules[data][rule])
            elif data == "configureable_rules":
                configureable_rules.append(rules[data][rule])
            elif data == "newlines_before_rules":
                newlines_before.append(rules[data][rule])
    return indent_begining_rules, indent_ending_rules, comment_rules, exclude_rules, newline_rules, configureable_rules, newlines_before

def main():
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Your LaTex document", type=str)
    parser.add_argument("--rules",help="Your config rules", type=str)
    parser.add_argument("--header",help="For info on what have been changed", action="store_true")
    args = parser.parse_args()
    if args.rules:
        if args.rules.lower().endswith(('.json')):
            rules = open(args.rules)
            data = json.loads(rules.read())
        elif args.rules.lower().endswith(('.yaml')):
            rules = open(args.rules)
            data = yaml.load(rules, Loader=yaml.FullLoader)
        else:
            print("Invalid input format. Only accepting .json or .yaml")
            sys.exit()
        rules.close()
    else:
        os_name = platform.system()
        here = pathlib.Path(__file__).parent
        if os_name == "Windows":
            rules = open(str(here.absolute()) + "\\rules.JSON")
        elif os_name == "Linux" or os_name == "Darwin":
            rules = open(str(here.home()) + "/.local/bin/rules.JSON")
        data = json.loads(rules.read())
        rules.close()
    if args.file.lower().endswith(('.tex', '.bib', 'tikz')):
        if args.header == True:
            tex_Linter(args.file, data, args.header)
        else:
            tex_Linter(args.file, data)
    else:
        print("Invalid input format. Only accepting .tex, .bib or .tikz")
        sys.exit()
    ext = args.file.rpartition('.')[-1]
    print("DONE AT ", (time.time() - start_time), "check Validated_file." + ext +" for fixed file")
    
if __name__ == '__main__':
    main()
