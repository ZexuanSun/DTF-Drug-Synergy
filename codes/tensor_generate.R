data = read.csv('drug_drug_synergy_original.csv')
#sub_data = subset(data,synergy == 0)
cell_line = data$cell_line
cell_line = factor(cell_line)
length(cell_line)
cell_line = sort(cell_line)
all_cell_line = levels(cell_line)
length(all_cell_line)







all_drug_a = levels(data$drug_a_name)#37
length(all_drug_a)

all_drug_b = levels(data$drug_b_name)#37
length(all_drug_b)
all_drug = union(all_drug_a,all_drug_b)

all_info = data 
for(i in 1:38)
{
        all_info$drug_b_name = gsub(pattern 
                                    = all_drug[i], i,all_info$drug_b_name)
        all_info$drug_a_name = gsub(pattern 
                                    = all_drug[i], i,all_info$drug_a_name)
}
all_info$drug_a_name = as.numeric(all_info$drug_a_name)
all_info$drug_b_name = as.numeric(all_info$drug_b_name)

# for(j in seq(1,23052,2))
#         for( i in j:(j+1))
#         {
#                 if
#         }







# ans = 0
# for(i in 1:23052)
# {
#         if(is.na(as.numeric(all_info$drug_b_name[i])))
#         {
#                 ans = ans +1
#         }
# }






ans = 0
for(p in 1: 39){
cell_line_tmp = subset(all_info,cell_line == all_cell_line[p])
# for(i in 1:604)
# {
#         if(is.na(as.numeric(cell_line_1$drug_b_name[i])))
#         {
#                 ans = ans +1
#         }
# }

set_del=(0)
tmp_r = nrow(cell_line_tmp)
if(tmp_r %% 2 )
        tmp_r = tmp_r - 1 
for( i in seq(1,tmp_r,2))
        {
                if(cell_line_tmp$drug_a_name[i] == cell_line_tmp$drug_a_name[i+1 ] &&
                   cell_line_tmp$drug_b_name[i] == cell_line_tmp$drug_b_name[i+1 ] )
                        {
                        cell_line_tmp$synergy[i+1] = 0.5*(cell_line_tmp$synergy[i] +
                                                                cell_line_tmp$synergy[i+1])
                        set_del = union(set_del,i)
                        
                }
}
if(tmp_r %% 2 )
        tmp_r = tmp_r + 1 
else
        tmp_r = tmp_r -1 
for( i in seq(2,tmp_r,2))
{
        if(cell_line_tmp$drug_a_name[i] == cell_line_tmp$drug_a_name[i+1 ] &&
           cell_line_tmp$drug_b_name[i] == cell_line_tmp$drug_b_name[i+1 ] )
        {
                cell_line_tmp$synergy[i+1] = 0.5*(cell_line_tmp$synergy[i] +
                                                        cell_line_tmp$synergy[i+1])
                set_del = union(set_del,i)
        }
}

set_del = setdiff(set_del,0)
if(length(set_del) > 0 )
        cell_line_tmp = cell_line_tmp[-set_del,]

#tmp_o = matrix(nrow = 38, ncol = 38,0)
tmp_o = matrix(nrow = 38, ncol = 38)
test_num = 37
ans = 0
for( i in 1:nrow(cell_line_tmp))
{
        tmp_o[cell_line_tmp$drug_a_name[i],
               cell_line_tmp$drug_b_name[i] ] = 
                cell_line_tmp$synergy[i]
        #sink('ans.txt')
        #print(tmp_o[as.numeric(cell_line_1$drug_a_name[i]),
                    #as.numeric(cell_line_1$drug_b_name[i])])
        #ans =ans + 1
        #print(ans)
        
        # if( is.na(tmp_o[as.numeric(cell_line_1$drug_a_name[i]),
        #                 as.numeric(cell_line_1$drug_b_name[i])]))
        #         print(i)
}
#print(sum(!is.na(tmp_o)))




for( i in 1:37)
        {
                #if(all_drug_a[i] == all_drug_b[i])
                        tmp_o[i,i] = 0
                
                for( j in (i+1):38){
                        if(!is.na(tmp_o[i,j]))
                                tmp_o[j,i] = tmp_o[i,j]
                        else if(!is.na(tmp_o[j,i]))
                                tmp_o[i,j] = tmp_o[j,i]
                }
        }

tmp_o[38,38] = 0

tmp_o[is.na(tmp_o)] = 0
name = paste('tensor_',p,'.csv',sep='')
write.csv(tmp_o,name)

}
