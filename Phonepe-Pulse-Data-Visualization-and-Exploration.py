import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px
import os
import json
from PIL import Image
  
#sql database
mydb= mysql.connector.connect(
    host ='localhost',
    user='root',
    password='',
    database = "phonepee"
)
mycursor=mydb.cursor(buffered=True)
mycursor.execute("USE phonepee")

icon = Image.open(r"E:\streamlit\images.png")
st.set_page_config(page_title= "PhonePe Pulse Data Visualization | By Samuel Solomon",
                   page_icon= icon,
                   layout= "wide")

# st.sidebar.header(":currency_exchange: :red[**Hello! Welcome to phonepe**]")
# Creating option menu in the side bar
with st.sidebar:
    selected = st.selectbox("**Menu**", ("Home","Top Charts","Explore Data","Explore Data1","about"))
# Menu == Home
if selected == "Home":
        image =Image.open("hp-banner1.png")
        st.image(image)
        colum3,colum4,colum5= st.columns([0.015,0.020,0.1])
        with colum3:
            if st.button("Phone_pe"):
                st.write("https://www.phonepe.com/")
        with colum4:
            if st.button("download_apk"):
                st.write("https://www.phonepe.com/app-download/")
        with colum5:
            if st.button("etc"):
                st.write("THANK YOU")   
            
        
        # video_file = open('star.mp4', 'rb')
        # video_bytes = video_file.read()

        # st.video(video_bytes)
        # age = st.slider('How old are you?', 2018,2022)
        # # st.write("I'm ", age, 'years old')

        colum3,colum4= st.columns([2,2])
        with colum3:
                video_file = open('home-fast-secure-v3.mp4', 'rb')
                video_bytes = video_file.read()

                st.video(video_bytes)
        with colum4:
            
            st.markdown('### Simple, Fast & Secure')
            st.markdown('#### :violet[ One app for all things money:] ')
            st.markdown("Pay bills, recharge, send money, buy gold, invest and shop at your favourite stores.")

            st.markdown("#### :violet[ Pay whenever you like, wherever you like:] ") 
            st.markdown("Choose from options like UPI, the PhonePe wallet or your Debit and Credit Card.")  

            st.markdown("#### :violet[ Find all your favourite apps on PhonePe Switch:] ")  
            st.markdown(" Book flights, order food or buy groceries. Use all your favourite apps without downloading them.")

#menu == top_charts
if selected =="Top Charts":
    # mycursor.execute('select Year, Quater,avg(Transaction_amount) from agg_transaction group by year,quater order by avg(Transaction_amount)')
    # mydb.commit()
    # df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    # fig = px.pie(df,
    #                  values=mycursor.column_names[2],
    #                  names=mycursor.column_names[0],
    #                  color=mycursor.column_names[0]
    #                 )
    # st.plotly_chart(fig,use_container_width=True)

    st.markdown("## Top Charts")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        year = st.slider("**Year**", min_value=2018, max_value=2022)
        quater = st.slider("**Quater**", min_value=1, max_value=4)
    
    with colum2:
            st.markdown('### explore  bar chart and sunburst chart  ')
            st.markdown('#### :red[using csv files:] ')
            st.markdown("using agg_transaction, map_tansaction, top_transaction, agg_user, map_user, top_user")

            st.markdown("#### :red[ top 10:] ") 
            st.markdown("this sql query is top 10 amount (or) count  in all state ")  
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        colum4,colum5,colum6 = st.columns([.5,.5,.5],gap="Small")
            #first pie
        with colum4:
            mycursor.execute(f'''select Year,Quater, State, sum(Transaction_count) as total_transaction_count, sum(Transaction_amount) as total_amount
                    from agg_transaction where  Year like {year} and Quater like {quater} group by State order by total_amount desc limit 10 ''')
            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            fig = px.pie(df, values='total_amount',
                names='State',
                title='agg_trans: top 10  transaction _amount',
                color_discrete_sequence=px.colors.sequential.Agsunset)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            # fig.show()
            st.plotly_chart(fig,use_container_width=True)
            #second pie     
        with colum5:    
            mycursor.execute(f'''select Year,Quater, district , sum(Count) as total_count, sum(amount) as total_amount from map_transaction 
                            where Year like {year} and Quater like {quater} group by district order by total_amount desc limit 10''')
            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            fig = px.pie(df, values='total_amount',
                            names='district',
                            title='map_trans: top 10  transaction _amount',
                            color_discrete_sequence=px.colors.sequential.Agsunset)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            # fig.show()
            st.plotly_chart(fig,use_container_width=True)
            #third pie
        with colum6:
            # mycursor.execute(f'''select Year,Quater,district , sum(Count) as total_count, sum(amount) as total_amount from top_transaction 
            #      where Year like {year} and Quater like {quater} group by district order by total_amount desc limit 10''')
            # df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            # # df
            # fig = px.pie(df, values='total_amount',
            #                 names='district',
            #                 color_discrete_sequence=px.colors.sequential.Agsunset)
            # fig.update_traces(textposition='inside', textinfo='percent+label')
            # # fig.show()
            # st.plotly_chart(fig,use_container_width=True)
            mycursor.execute(f'''select state,Year,Quater,district , sum(Count) as total_count, sum(amount) as total_amount from top_transaction 
                 where Year like {year} and Quater like {quater} group by district order by total_amount desc limit 10''')
            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            # print(df)
            fig = px.sunburst(df, values='total_amount',
                        path=['Year','state','district','total_amount'],
                            color='state',
                            title='top_trans: top 10 transaction_amount',
                            # textinfo= 'label+values',

                            color_discrete_sequence=px.colors.sequential.Agsunset)

            st.plotly_chart(fig,use_container_width=True)
            # fig.show()
# Top Charts == Users    
             
    if Type == "Users":
        colum4,colum6 = st.columns([.5,.5],gap="Small")
        with colum4:
            mycursor.execute(f"""
            select State,Year,Quater,Brands,sum(Count) as total_count,sum(Percentage) as total_percentage 
            from agg_user where year like {year} and Quater like {quater} group by State, Year order by total_count limit 10

            """)
            mydb.commit()

            df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
            # df
            fig = px.pie(df, values='total_count',
                names="State",
                title='agg_user: top 10  transaction_count',
                color_discrete_sequence=px.colors.sequential.Agsunset)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            # fig.show()
            st.plotly_chart(fig,use_container_width=True)
        #     fig = px.sunburst(df, values='total_count',
        #                 path=["Year",'State','Brands','total_count'],
        #                     color='Brands',
        #                     title="agg_user to 10 brand "
        #                     color_discrete_sequence=px.colors.sequential.Agsunset)

        #     st.plotly_chart(fig,use_container_width=True)
        # # fig.show()
        with colum6:
            mycursor.execute(f'''select State,year,quater,district_name as district, sum(registeredUsers) as total_user,
                    pincode  from top_user where year like {year} and quater like {quater} group by state order by total_user limit 10''')
            mydb.commit()

            df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
            # df

            fig = px.sunburst(df, values='total_user',
                        path=["year",'State','district','pincode','total_user'],
                            color='district',
                            title="top_user: top 10 user_count show in district pincode",
                            color_discrete_sequence=px.colors.sequential.Agsunset)

            st.plotly_chart(fig,use_container_width=True)
            # fig.show()
#menu == explore Data
if selected == 'Explore Data':
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users","Users1"))
    
#explore Data = "transactions"

    if  Type == 'Transactions':
        year = st.slider("**Year**", min_value=2018, max_value=2022)
        quater = st.slider("**Quater**", min_value=1, max_value=4)

        selected_state = st.selectbox("",
                                    ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                                    'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                    'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                                    'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                                    'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                    'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
                
        mycursor.execute(f"""select State, District,year,quater, sum(count) as Total_Transactions, sum(amount) as Total_amount 
                            from map_transaction where year = {year} and quater = {quater} and State = '{selected_state}' group by State,
                            District,year,quater order by state,district""")
                
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        fig = px.bar(df,
                    title=selected_state,
                    x="District",
                    y="Total_amount",
                    orientation='v',
                    color='Total_Transactions',
                color_continuous_scale=px.colors.sequential.Agsunset)
        # fig.show()
        st.plotly_chart(fig,use_container_width=True)
        
 #explore Data = "users"
            
    if Type == "Users":
        year = st.slider("**Year**", min_value=2018, max_value=2022)
        quater = st.slider("**Quater**", min_value=1, max_value=4)

        selected_state = st.selectbox("",
                                   ("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh",
                                    "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir",
                                    "Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Mizoram",
                                    "Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
                                    "Uttar Pradesh","Uttarakhand","West Bengal"),index=30)



        mycursor.execute(f"""select State, district,year,quater, sum(registeredUsers) as Total_registration ,sum(appOpens) as total_app_user
                            from map_user where year like {year} and quater like {quater} and State like '{selected_state}'
                            group by State,district,year,quater order by state,district  """)
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        fig = px.bar(df,
                    title=selected_state,
                    x="district",
                    y="Total_registration",
                    color='Total_registration',
                color_continuous_scale=px.colors.sequential.Agsunset)
        # fig.show()
        st.plotly_chart(fig,use_container_width=True)
        # fig = px.sunburst(df, values='Total_registration',
        #             path=['State',"district",'Total_registration'],
        #                 color='district',
        #                 color_discrete_sequence=px.colors.sequential.Agsunset)

        # st.plotly_chart(fig,use_container_width=True)
        
 #explore Data = "users1"

    if Type == "Users1":
        year = st.slider("**Year**", min_value=2018, max_value=2022)
        quater = st.slider("**Quater**", min_value=1, max_value=4)

        selected_state = st.selectbox("",
                                   ("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh",
                                    "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir",
                                    "Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Mizoram",
                                    "Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
                                    "Uttar Pradesh","Uttarakhand","West Bengal"),index=30)



        mycursor.execute(f"""select State, district,year,quater, sum(registeredUsers) as Total_registration ,sum(appOpens) as total_app_user
                            from map_user where year like {year} and quater like {quater} and State like '{selected_state}'
                            group by State,district,year,quater order by state,district  """)
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        # fig = px.bar(df,
        #             title=selected_state,
        #             x="district",
        #             y="Total_registration",
        #             color='Total_registration',
        #         color_continuous_scale=px.colors.sequential.Agsunset)
        # # fig.show()
        # st.plotly_chart(fig,use_container_width=True)
        fig = px.sunburst(df, values='Total_registration',
                    path=['State',"district",'Total_registration','total_app_user'],
                        color='district',
                        title=selected_state,
                        color_discrete_sequence=px.colors.sequential.Agsunset)

        st.plotly_chart(fig,use_container_width=True)
        
#menu == "explore Data1"                
        
if selected == 'Explore Data1':
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    
 #explore Data1 = "tranasactions"

    if Type=='Transactions':
        colum4,colum5 = st.columns([.5,.5],gap="Small")
        with colum4:

            mycursor.execute('''select State,
                sum(Transaction_amount) as total_amount from  agg_transaction group by State   ''')
            mydb.commit()

            df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
            df

        with colum5:
            mycursor.execute('''select State,sum(Transaction_count) as total_count ,
                sum(Transaction_amount) as total_amount from  agg_transaction group by State   ''')
            mydb.commit()

            df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)

            fig = px.choropleth( 
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                title="agg_transaction state wise total_amount",
                locations='State',
                color='total_amount',
                color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_geos(fitbounds="locations", visible=False)
            # fig.show()
            st.plotly_chart(fig,use_container_width=True)

            
            
            
        colum4,colum5 = st.columns([.5,.5],gap="Small")    
        with colum4:
            mycursor.execute('''select State,sum(Transaction_count) as total_count from  agg_transaction group by State  order by total_count desc ''')
            mydb.commit()

            df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
            df
        with colum5:

            mycursor.execute('''select State,sum(Transaction_count) as total_count ,
                sum(Transaction_amount) as total_amount from  agg_transaction group by State  order by total_count desc ''')
            mydb.commit()

            df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)

            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                title="agg_transaction state wise total_User_count",
                locations='State',
                color='total_count',
                color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_geos(fitbounds="locations", visible=False)
            # fig.show()
            st.plotly_chart(fig,use_container_width=True)
            
 #explore Data1 = "users"
            
    if Type=='Users':
        colum4,colum5 = st.columns([.5,.5],gap="Small")
        with colum4:
            mycursor.execute('''select State,sum(count) as total_count from  agg_user group by State order by total_count desc ''')
            mydb.commit()

            df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
            df
        with colum5:
            mycursor.execute('''select State,Brands,sum(count) as total_count from  agg_user group by State order by total_count desc''')
            mydb.commit()

            df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
            # df

            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='total_count',
                title="state wise:\
                total_user_count using in agg_user",
                color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_geos(fitbounds="locations", visible=False)
            # fig.show()   
            st.plotly_chart(fig,use_container_width=True)
        colum4,colum5 = st.columns([.5,.5],gap="Small")   
        with colum4:
            mycursor.execute('''select State,sum(registeredUsers) as total_user_count from  map_user group by State  order by total_user_count  desc''')
            mydb.commit()

            df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
            df
        with colum5:
            mycursor.execute('''select State,sum(registeredUsers) as total_user_count from  map_user group by State order by total_user_count  desc''')
            mydb.commit()

            df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                title="state wise : \
                total_user_count using in map_user", 

                color='total_user_count',
                color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_geos(fitbounds="locations", visible=False)
            # fig.show()
            st.plotly_chart(fig,use_container_width=True)
            
#menu about
            
if selected == "about":
    st.markdown('### PhonePe Terms & Conditions')
    st.markdown("""This document is an electronic record in terms of Information Technology Act, 2000,
                amendments thereof from time to time and the rules thereunder as applicable and the amended 
                provisions pertaining to electronic records in various statutes as amended by the Information Technology Act, 2000.
                This electronic record is generated by a computer system and does not require any physical or digital signatures.""")
    st.markdown("""Please read the terms and conditions carefully before registering, accessing or using the PhonePe Services (defined below).
                The terms and conditions are legal contract ("Agreement") between You and PhonePe Private Limited (“PhonePe”)
                having its registered office at Unit No.001, Ground Floor, Boston House, Suren Road, Off. Andheri-Kurla Road,
                Andheri (East) Mumbai – 400 093, India. You agree and acknowledge that you have read the terms and conditions set forth below.
                If you do not agree to these terms and conditions or do not wish to be bound by these terms and conditions,
                you may not use the Services and/or immediately terminate the Services and/or uninstall the mobile application.""")
    st.markdown("""We may amend the terms and conditions at any time by posting an updated version at PhonePe website(s) and PhonePe App(s).
                The updated version of the Terms of Service shall take effect immediately upon posting. It is Your responsibility to
                review these Terms of Use periodically for updates / changes. Your continued use of PhonePe App following the 
                posting of changes will mean that You accept and agree to the revisions including additional Terms or removal of
                portions of these Terms, modifications etc. As long as You comply with these Terms of Use, We grant You a personal,
                non-exclusive, non-transferable, limited privilege to enter and avail the Services.""")
    st.markdown("""USING PHONEPE APP INDICATES YOUR AGREEMENT TO ALL THE TERMS AND CONDITIONS UNDER THESE TERMS OF USE,
                SO PLEASE READ THE TERMS OF USE CAREFULLY BEFORE PROCEEDING. By impliedly or expressly accepting these Terms of Use, 
                You also accept and agree to be bound by PhonePe and PhonePe Entity Policies (including but not limited to Privacy Policy)
                available on the PhonePe website(s) and PhonePe App(s) as amended from time to time.""")
    st.markdown('#### :black[github:]')
    st.markdown('https://github.com/Muthukumar0908/Phonepe-Pulse-Data-Visualization-and-Exploration.git')
    













            

    