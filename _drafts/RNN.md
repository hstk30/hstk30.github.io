## RNN

\\[ output_t = W \cdot input_t + U \cdot state_t + bia \\]
\\[ state_{t+1} = output_t \\]

## LSTM


\\[ i_t = W_i \cdot input_t + U_i \cdot state_t + bia_i \\]
\\[ f_t = W_f \cdot input_t + U_f \cdot state_t + bia_f \\]
\\[ tmp = W_c \cdot input_t + U_c \cdot state_t + bia_c \\]
\\[ c_{t+1} = f_t * c_t + i_t * tmp \\]
\\[ o_t = W_o \cdot input_t + U_o \cdot state_t + bia_o \\]
\\[ output_t = o_t * c_{t+1} \\]
\\[ state_{t+1} = output_t \\]
