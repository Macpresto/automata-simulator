
from automata.fa.dfa import DFA
from visual_automata.fa.dfa import VisualDFA
import pandas as pd 
import streamlit as sl

#DFA regex1
dfa1 = DFA(
states= {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9',
 'q10', 'q11', 'q12', 'q13', 'q14', 'TRAP'},
input_symbols={'A','B'},
transitions={
    'q0':{'A':'q1','B':'q2'},
    'q1':{'A':'q5','B':'q6'},
    'q2':{'A':'q3','B':'q6'},
    'q3':{'A':'TRAP','B':'q4'},
    'q4':{'A':'q9','B':'q2'},
    'q5':{'A':'TRAP','B':'q7'},
    'q6':{'A':'q8', 'B':'TRAP'},
    'q7':{'A':'q9', 'B':'TRAP'},
    'q8':{'A':'TRAP','B':'q9'},
    'q9':{'A':'q10','B':'q10'},
    'q10':{'A':'q11','B':'q12'},
    'q11':{'A':'q13','B':'q12'},
    'q12':{'A':'q11','B':'q14'},
    'q13':{'A':'q13','B':'q12'},
    'q14':{'A':'q11','B':'q14'},
    'TRAP':{'A':'TRAP','B':'TRAP'},
},
initial_state='q0',
final_states={'q13', 'q14'}
)

#DFA regex2
dfa2 = DFA(
states= {'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9',
 'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17',},
input_symbols={'1','0'},
transitions={
    'q1':{'0':'q2','1':'q3'},
    'q2':{'0':'q4','1':'q3'},
    'q3':{'0':'q2','1':'q4'},
    'q4':{'0':'q5','1':'q5'},
    'q5':{'0':'q5','1':'q6'},
    'q6':{'0':'q8', '1':'q7'},
    'q7':{'0':'q8', '1':'q17'},
    'q8':{'0':'q5','1':'q10'},
    'q9':{'0':'q9','1':'q6'},
    'q10':{'0':'q13','1':'q11'},
    'q11':{'0':'q12','1':'q17'},
    'q12':{'0':'q9','1':'q10'},
    'q13':{'0':'q14','1':'q10'},
    'q14':{'0':'q14','1':'q15'},
    'q15':{'0':'q8','1':'q16'},
    'q16':{'0':'q8','1':'q17'},
    'q17':{'0':'q13','1':'q17'},
},
initial_state='q1',
final_states={'q9', 'q10', 'q11', 'q12', 'q13','q14', 'q15', 'q16', 'q17'}
)

###################################################################################################
#                                     USER INTERFACE                                              #
###################################################################################################

sl.set_page_config(
    page_icon="🦈",
    layout="wide",
 )
sl.title("Automata")

#varaible declaration for regular expressions
reg_ex1 = '(bab)*(b+a)(bab+aba)(a+b)*(aa+bb)*(b+a+bb)(a+b)*(aa+bb)'
rex_ex2 = '(1+0)*(11+00)(00+11)*(1+0+11)(1+0+11)*(101+111)(101+111)*(1+0*+11)(1+0*+11)'

#select box for regular expression
input_box = sl.selectbox("Select Expression:", (reg_ex1, rex_ex2)) 

# Page Control
# User input Box


#cfg image
dfa_slot = sl.empty()
col3, col4 = sl.beta_columns(2)
cfg_slot = col3.empty()


if input_box == reg_ex1:
    dfa = dfa1 
    with cfg_slot.beta_expander("CFG", expanded = True):
        sl.write("""
         S -> PQRTUVXY\n
         P -> babP|λ\n
         Q -> b|a\n
         R -> bab|aba\n
         T -> aT|bT|λ\n
         U -> aaU|bbU|λ\n
         V -> b|a|bb\n
         X -> aX|bX|λ\n
         Y -> aa|bb\n
    """)

else:
    dfa = dfa2
    with cfg_slot.beta_expander("CFG", expanded = True):
        sl.write("""
         S -> PQRTUVWYY\n
         P -> 1P|0P|λ\n
         Q -> 11|00\n
         R -> 00R|11R|λ\n
         T -> 1|011\n
         U -> 1U|0U|11U|λ\n
         V -> 101|111\n
         W -> 101W|111W|λ\n
         Y -> 1|X|11\n
         X -> 0X|λ\n
    """)

form = col4.form(key="form")
user_input = form.text_input(label="Enter String To Check If Valid:").upper()
if not user_input:
    col4.warning("Please fill out so required fields")

submit = form.form_submit_button(label="Simulate")

visual_dfa = VisualDFA(dfa)
with sl.form("dfa_form"):
    dfa_slot.write(visual_dfa.show_diagram())

#sl.write(type(submit))
if user_input:
    try:
        if submit:
            if(dfa.accepts_input(user_input)):
                col4.success('Valid!')
            else:
                col4.error('Invalid!')
                
            
            col1, col2 = sl.beta_columns(2)
            visual_dfa = VisualDFA(dfa)
            str_user_input = str(user_input)
            dfa_slot.write(visual_dfa.show_diagram(str_user_input))

            dfa1_final_states =['*q13', '*q14']
            dfa2_final_states =['*q9', '*q10', '*q11', '*q12', '*q13','*q14', '*q15',
            '*q16', '*q17']
            x = visual_dfa.input_check(user_input)

            #check input per step and append reject or accept
            listy = []
            for i in x.iloc[:,2]:
                if i == "TRAP":
                    listy.append("Rejected")
                else:
                    listy.append("Accepted")

            index = len(user_input) #check user input length
            x_list = x.iloc[:,1].tolist() #create list of input

            #check if finished or did not finish
            if dfa == dfa1:
                if str(x.iloc[index-1,2]) in dfa1_final_states:
                    listy.append("Finished")
                else:
                    listy.append("DID NOT FINISH")
                    #sl.write(str(x.iloc[index-1,2]))
            elif dfa == dfa2:
                if x.iloc[index-1,2] in dfa2_final_states:
                    listy.append("Finished")
                else:
                    listy.append("DID NOT FINISH") 

            x_list.append('END')
            #data frame for step checking
            col4.write('#### Tracking')
            col4.write(pd.DataFrame({'Input': x_list,
            'evaluation': listy,
            }))


            
    except:
        sl.write(" ")

else:
    sl.write(" ")
