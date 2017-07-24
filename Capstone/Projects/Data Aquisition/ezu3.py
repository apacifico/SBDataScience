##################################### ezu3.py ######################################
#  3rd version, with counters available on FIO6 and FIO7    4/3/2015
#  Halverson's easy interface to the LabJack U3 for student use.
#  2nd version.  (Version 1 was called easyU3.py)   2/1/2015
#
#  Available functions:   u3setup, LED, turnLEDoff, turnLEDon, 
#  dac0out, dac1out, dac0out8, dac1out8, 
#  ain0, ain1,..., ain7             (analog inputs via the FIO connectors)
#  din0, din1,..., din7             (digital inputs via the FIO connectors)
#  dout0, dout1,..., dout7          (digital outputs via the FIO connectors)
#  temperatureC, temperatureF
#  u3_add_ctr6(d):                  #Adds a single counter, to FIO6
#  u3_add_ctr7(d):                  #Adds a single counter, to FIO7
#  u3_add_ctr6_and_7(d):            #Adds two counters, to FIO6 and FIO7

#  Added 5/3/2015:
#  ainE0, ainE1,..., ainE7             (analog inputs via the EIO db-15 connector)
#  dinE0, dinE1,..., dinE7             (digital inputs via the EIO db-15 connector)
#  doutE0, doutE1,..., doutE7          (digital outputs via the EIO db-15 connector)
#  dinC0, dinC1,dinC2,dinC3            (digital inputs via the CIO on the db-15 connector)
#  doutC0, doutC1, doutC2, doutC3      (digital outputs via the CIO on the db-15 connect

# DB-15 pin connections:
# 1=VS (+5 Volts), 2=CIO1, 3=CIO3, 4=EIO0, 5=EIO2, 6=EIO4, 7=EIO6, 8=GND
# 9=CIO0, 10=CIO2, 11=GND, 12=EIO1, 13=EIO3, 14=EIO5, 15=EIO7

#
import u3
def u3setup(d,u3channels,u3channelsE=None,u3channelsC=None):
    global u3channels_saved
    global u3channels_savedE        # For the eight EIO channels on the DB-15 connector
    global u3channels_savedC        # For the four CIO channels  on the DB-15 connector
    u3channels_savedE = u3channelsE
    u3channels_savedC = u3channelsC
    u3channels_saved=u3channels
    print "Opening LabJack U3 device..."
    # For applying the proper calibration to readings.  (Next line is optional)
    d.getCalibrationData()   
    analog_input_bits = 0
    for i in range(0,8):
      if u3channels[i] == 'ain':
        print "Setting FIO",i," to be analog input ain"+str(i)," Analog input range is 0 to 2.4 volts"
        analog_input_bits = analog_input_bits + (1 << i)
      elif u3channels[i] == 'din':
        print "Setting FIO",i," to be digital input din"+str(i)
        d.getDIState(i)
      elif u3channels[i] == 'dout':
        print "Setting FIO",i," to be digital output dout"+str(i)
        d.setFIOState(i, state = 0)
      else:
        print "Something is wrong with the string that defines what the FIO channels should do."
        print "This is what you gave me:"
        print u3channels
        raise RuntimeError('Sorry...')
    if u3channelsE != None:
       analog_input_bitsE = 0
       for i in range(0,8):
         if u3channelsE[i] == 'ain':
           print "Setting EIO",i," to be EIO analog input ain"+str(i)," Analog input range is 0 to 2.4 volts"
           analog_input_bitsE = analog_input_bitsE + (1 << i)
         elif u3channelsE[i] == 'din':
           print "Setting EIO",i," to be EIO digital input din"+str(i)
           d.getDIState(8+i)
         elif u3channelsE[i] == 'dout':
           print "Setting EIO",i," to be EIO digital output dout"+str(i)
           d.setFIOState(8+i, state = 0)
         else:
           print "Something is wrong with the string that defines what the EIO channels should do."
           print "This is what you gave me:"
           print u3channelsE
           raise RuntimeError('Sorry...')
         d.configIO(EIOAnalog = analog_input_bitsE)
    if u3channelsC != None:
       for i in range(0,4):
         if u3channelsC[i] == 'din':
           print "Setting CIO",i," to be CIO digital input din"+str(i)
           d.getDIState(16+i)
         elif u3channelsC[i] == 'dout':
           print "Setting CIO",i," to be CIO digital output dout"+str(i)
           d.setFIOState(16+i, state = 0)
         else:
           print "Something is wrong with the string that defines what the CIO channels should do."
           print "This is what you gave me:"
           print u3channelsC
           raise RuntimeError('Sorry...')    
    d.configIO(FIOAnalog = analog_input_bits)

def u3_add_ctr6(d):              #Adds a single counter, to FIO6
  global u3channels_saved
  if u3channels_saved.count('ctr') ==0:
    if u3channels_saved[6] == 'din':
      print "Setting FIO6 to be a counter"
      d.configIO(EnableCounter0 = True, TimerCounterPinOffset =6)  #Put counter 0 on to FIO6
      u3channels_saved[6] = 'ctr'
    else:
      print "Before you can make FIO6 into a counter, you must first make into a digital input."
      print "Right now FIO6 is configured as: ",u3channels_saved[6]
      raise RuntimeError('Sorry...')
  else:
    print "If you want more that one counter, use the u3_add_ctr6_and_7 function.  You can't"
    print "create one counter and then create another.  The max number of counters is two."
    raise RuntimeError('Sorry...')    
def u3_add_ctr7(d):              #Adds a single counter, to FIO7
  global u3channels_saved
  if u3channels_saved.count('ctr') ==0:
    if u3channels_saved[7] == 'din':
      print "Setting FIO7 to be a counter"
      d.configIO(EnableCounter0 = True, TimerCounterPinOffset =7)  #Put counter 0 on to FIO7
      u3channels_saved[7] = 'ctr'
    else:
      print "Before you can make FIO7 into a counter, you must first make into a digital input."
      print "Right now FIO7 is configured as: ",u3channels_saved[7]
      raise RuntimeError('Sorry...')
  else:
    print "If you want more that one counter, use the u3_add_ctr6_and_7 function.  You can't"
    print "create one counter and then create another.  The max number of counters is two."
    raise RuntimeError('Sorry...')    
def u3_add_ctr6_and_7(d):              #Adds two counters, to FIO6 and FIO7
  global u3channels_saved
  if (u3channels_saved[6] == 'din') & (u3channels_saved[7] == 'din'):
    print "Setting FIO6 and FIO7 to be counters"
    d.configIO(EnableCounter0 = True, EnableCounter1 = True, TimerCounterPinOffset =6)  #Put counter 0 on to FIO6, counter 1 on FIO7
    u3channels_saved[6] = 'ctr'
    u3channels_saved[7] = 'ctr'
  else:
    print "Before you can make FIO6 and FIO7 into counters, you must first make them into digital inputs."
    print "Right now FIO6 is configured as ",u3channels_saved[6],"  and FIO7 is configured as ",u3channels_saved[7]
    raise RuntimeError('Sorry...')
################################## Built-in LED ################################
def LED(d,on_or_off = True):     #If on_or_off is True, then the LED will turn on.
   d.getFeedback(u3.LED(State = on_or_off))
def turnLEDoff(d):
   d.getFeedback(u3.LED(State = False))
def turnLEDon(d):
   d.getFeedback(u3.LED(State = True))
################################## ANALOG OUTPUT 16 bit version ################################
def dac0out(d,v=0.0):    # v is the floating point voltage.  Range is 0 to 4.95 
   DAC0_VALUE = d.voltageToDACBits(v, dacNumber = 0, is16Bits = True)
   d.getFeedback(u3.DAC0_16(DAC0_VALUE))        # Set DAC0 to v Volts
def dac1out(d,v=0.0):    # v is the floating point voltage.  Range is 0 to 4.95 
   DAC1_VALUE = d.voltageToDACBits(v, dacNumber = 1, is16Bits = True)
   d.getFeedback(u3.DAC1_16(DAC1_VALUE))        # Set DAC1 to v Volts
################################## ANALOG OUTPUT 8 bit version ################################
def dac0out8(d,v=0.0):    # v is the floating point voltage.  Range is 0 to 4.95 
   DAC0_VALUE = d.voltageToDACBits(v, dacNumber = 0, is16Bits = False)
   d.getFeedback(u3.DAC0_8(DAC0_VALUE))        # Set DAC0 to v Volts
def dac1out8(d,v=0.0):    # v is the floating point voltage.  Range is 0 to 4.95 
   DAC1_VALUE = d.voltageToDACBits(v, dacNumber = 1, is16Bits = False)
   d.getFeedback(u3.DAC1_8(DAC1_VALUE))        # Set DAC1 to v Volts
################################## ANALOG INPUT ################################
def ain0(d):
  global u3channels_saved
  i=0
  if u3channels_saved[i] == 'ain':
    return d.getAIN( i )
  else:
    print "Error trying to get analog data from FIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ain1(d):
  global u3channels_saved
  i=1
  if u3channels_saved[i] == 'ain':
    return d.getAIN( i )
  else:
    print "Error trying to get analog data from FIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ain2(d):
  global u3channels_saved
  i=2
  if u3channels_saved[i] == 'ain':
    return d.getAIN( i )
  else:
    print "Error trying to get analog data from FIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ain3(d):
  global u3channels_saved
  i=3
  if u3channels_saved[i] == 'ain':
    return d.getAIN( i )
  else:
    print "Error trying to get analog data from FIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ain4(d):
  global u3channels_saved
  i=4
  if u3channels_saved[i] == 'ain':
    return d.getAIN( i )
  else:
    print "Error trying to get analog data from FIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ain5(d):
  global u3channels_saved
  i=5
  if u3channels_saved[i] == 'ain':
    return d.getAIN( i )
  else:
    print "Error trying to get analog data from FIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ain6(d):
  global u3channels_saved
  i=6
  if u3channels_saved[i] == 'ain':
    return d.getAIN( i )
  else:
    print "Error trying to get analog data from FIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ain7(d):
  global u3channels_saved
  i=7
  if u3channels_saved[i] == 'ain':
    return d.getAIN( i )
  else:
    print "Error trying to get analog data from FIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
################################## DIGITAL INPUT ################################
def din0(d):
  global u3channels_saved
  i=0
  if u3channels_saved[i] == 'din':
    return d.getDIState(i)==1
  else:
    print "Error trying to get digital data from FIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def din1(d):
  global u3channels_saved
  i=1
  if u3channels_saved[i] == 'din':
    return d.getDIState(i)==1
  else:
    print "Error trying to get digital data from FIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def din2(d):
  global u3channels_saved
  i=2
  if u3channels_saved[i] == 'din':
    return d.getDIState(i)==1
  else:
    print "Error trying to get digital data from FIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def din3(d):
  global u3channels_saved
  i=3
  if u3channels_saved[i] == 'din':
    return d.getDIState(i)==1
  else:
    print "Error trying to get digital data from FIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def din4(d):
  global u3channels_saved
  i=4
  if u3channels_saved[i] == 'din':
    return d.getDIState(i)==1
  else:
    print "Error trying to get digital data from FIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def din5(d):
  global u3channels_saved
  i=5
  if u3channels_saved[i] == 'din':
    return d.getDIState(i)==1
  else:
    print "Error trying to get digital data from FIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def din6(d):
  global u3channels_saved
  i=6
  if u3channels_saved[i] == 'din':
    return d.getDIState(i)==1
  else:
    print "Error trying to get digital data from FIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def din7(d):
  global u3channels_saved
  i=7
  if u3channels_saved[i] == 'din':
    return d.getDIState(i)==1
  else:
    print "Error trying to get digital data from FIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
################################## COUNTER INPUT ################################
def ctr6(d):
  global u3channels_saved
  i=6
  if u3channels_saved[i] == 'ctr':
    return d.getFeedback(u3.Counter0( Reset = True ) )
  else:
    print "Error trying to get counter data from FIO"+str(i)+".  You didn't set it up for counter input."
    print "ctr"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ctr7(d):
  global u3channels_saved
  i=7
  if u3channels_saved[i] == 'ctr':
    if u3channels_saved[6] == 'ctr':           #Then there are two counters, so FIO7 is counter 1 and FIO6 is counter 0
      return d.getFeedback(u3.Counter1( Reset = True ) )
    else:
      return d.getFeedback(u3.Counter0( Reset = True ) )
  else:
    print "Error trying to get counter data from FIO"+str(i)+".  You didn't set it up for counter input."
    print "ctr"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
################################## DIGITAL OUTPUT ################################
def dout0(d,True_or_False = False):
  global u3channels_saved
  i=0
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_saved[i] == 'dout':
    d.setFIOState(i, state = zero_or_one)
  else:
    print "Error trying to send digital data to FIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def dout1(d,True_or_False = False):
  global u3channels_saved
  i=1
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_saved[i] == 'dout':
    d.setFIOState(i, state = zero_or_one)
  else:
    print "Error trying to send digital data to FIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def dout2(d,True_or_False = False):
  global u3channels_saved
  i=2
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_saved[i] == 'dout':
    d.setFIOState(i, state = zero_or_one)
  else:
    print "Error trying to send digital data to FIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def dout3(d,True_or_False = False):
  global u3channels_saved
  i=3
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_saved[i] == 'dout':
    d.setFIOState(i, state = zero_or_one)
  else:
    print "Error trying to send digital data to FIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def dout4(d,True_or_False = False):
  global u3channels_saved
  i=4
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_saved[i] == 'dout':
    d.setFIOState(i, state = zero_or_one)
  else:
    print "Error trying to send digital data to FIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def dout5(d,True_or_False = False):
  global u3channels_saved
  i=5
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_saved[i] == 'dout':
    d.setFIOState(i, state = zero_or_one)
  else:
    print "Error trying to send digital data to FIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def dout6(d,True_or_False = False):
  global u3channels_saved
  i=6
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_saved[i] == 'dout':
    d.setFIOState(i, state = zero_or_one)
  else:
    print "Error trying to send digital data to FIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def dout7(d,True_or_False):
  global u3channels_saved
  i=7
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_saved[i] == 'dout':
    d.setFIOState(i, state = zero_or_one)
  else:
    print "Error trying to send digital data to FIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
################################## TEMPERATURE ################################
def temperatureC(d):
   return d.getTemperature()-273.16                 #Converting Kelvins to Celsius by subtracting 273.16
def temperatureF(d):
   return (d.getTemperature()-273.16)*9.0/5.0+32.0  #Converting Kelvins to Celsius by subtracting 273.16






################################## ANALOG INPUT EIO ################################
def ainE0(d):
  global u3channels_savedE
  i=0
  if u3channels_savedE[i] == 'ain':
    return d.getAIN( 8+i )
  else:
    print "Error trying to get analog data from EIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ainE1(d):
  global u3channels_savedE
  i=1
  if u3channels_savedE[i] == 'ain':
    return d.getAIN( 8+i )
  else:
    print "Error trying to get analog data from EIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ainE2(d):
  global u3channels_savedE
  i=2
  if u3channels_savedE[i] == 'ain':
    return d.getAIN( 8+i )
  else:
    print "Error trying to get analog data from EIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ainE3(d):
  global u3channels_savedE
  i=3
  if u3channels_savedE[i] == 'ain':
    return d.getAIN( 8+i )
  else:
    print "Error trying to get analog data from EIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ainE4(d):
  global u3channels_savedE
  i=4
  if u3channels_savedE[i] == 'ain':
    return d.getAIN( 8+i )
  else:
    print "Error trying to get analog data from EIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ainE5(d):
  global u3channels_savedE
  i=5
  if u3channels_savedE[i] == 'ain':
    return d.getAIN( 8+i )
  else:
    print "Error trying to get analog data from EIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ainE6(d):
  global u3channels_savedE
  i=6
  if u3channels_savedE[i] == 'ain':
    return d.getAIN( 8+i )
  else:
    print "Error trying to get analog data from EIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def ainE7(d):
  global u3channels_savedE
  i=7
  if u3channels_savedE[i] == 'ain':
    return d.getAIN( 8+i )
  else:
    print "Error trying to get analog data from EIO"+str(i)+".  You didn't set it up for analog input."
    print "ain"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
################################## DIGITAL INPUT EIO ################################
def dinE0(d):
  global u3channels_savedE
  i=0
  if u3channels_savedE[i] == 'din':
    return d.getDIState(8+i)==1
  else:
    print "Error trying to get digital data from EIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def dinE1(d):
  global u3channels_savedE
  i=1
  if u3channels_savedE[i] == 'din':
    return d.getDIState(8+i)==1
  else:
    print "Error trying to get digital data from EIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def dinE2(d):
  global u3channels_savedE
  i=2
  if u3channels_savedE[i] == 'din':
    return d.getDIState(8+i)==1
  else:
    print "Error trying to get digital data from EIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def dinE3(d):
  global u3channels_savedE
  i=3
  if u3channels_savedE[i] == 'din':
    return d.getDIState(8+i)==1
  else:
    print "Error trying to get digital data from EIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def dinE4(d):
  global u3channels_savedE
  i=4
  if u3channels_savedE[i] == 'din':
    return d.getDIState(8+i)==1
  else:
    print "Error trying to get digital data from EIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def dinE5(d):
  global u3channels_savedE
  i=5
  if u3channels_savedE[i] == 'din':
    return d.getDIState(8+i)==1
  else:
    print "Error trying to get digital data from EIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def dinE6(d):
  global u3channels_savedE
  i=6
  if u3channels_savedE[i] == 'din':
    return d.getDIState(8+i)==1
  else:
    print "Error trying to get digital data from EIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def dinE7(d):
  global u3channels_savedE
  i=7
  if u3channels_savedE[i] == 'din':
    return d.getDIState(8+i)==1
  else:
    print "Error trying to get digital data from EIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
################################## DIGITAL OUTPUT EIO ################################
def doutE0(d,True_or_False = False):
  global u3channels_savedE
  i=0
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedE[i] == 'dout':
    d.setFIOState(8+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to EIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def doutE1(d,True_or_False = False):
  global u3channels_savedE
  i=1
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedE[i] == 'dout':
    d.setFIOState(8+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to EIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def doutE2(d,True_or_False = False):
  global u3channels_savedE
  i=2
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedE[i] == 'dout':
    d.setFIOState(8+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to EIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def doutE3(d,True_or_False = False):
  global u3channels_savedE
  i=3
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedE[i] == 'dout':
    d.setFIOState(8+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to EIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def doutE4(d,True_or_False = False):
  global u3channels_savedE
  i=4
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedE[i] == 'dout':
    d.setFIOState(8+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to EIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def doutE5(d,True_or_False = False):
  global u3channels_savedE
  i=5
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedE[i] == 'dout':
    d.setFIOState(8+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to EIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def doutE6(d,True_or_False = False):
  global u3channels_savedE
  i=6
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedE[i] == 'dout':
    d.setFIOState(8+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to EIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def doutE7(d,True_or_False):
  global u3channels_savedE
  i=7
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedE[i] == 'dout':
    d.setFIOState(8+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to EIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()





################################## DIGITAL INPUT CIO ################################
def dinC0(d):
  global u3channels_savedC
  i=0
  if u3channels_savedC[i] == 'din':
    return d.getDIState(16+i)==1
  else:
    print "Error trying to get digital data from CIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def dinC1(d):
  global u3channels_savedC
  i=1
  if u3channels_savedC[i] == 'din':
    return d.getDIState(16+i)==1
  else:
    print "Error trying to get digital data from CIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def dinC2(d):
  global u3channels_savedC
  i=2
  if u3channels_savedC[i] == 'din':
    return d.getDIState(16+i)==1
  else:
    print "Error trying to get digital data from CIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
def dinC3(d):
  global u3channels_savedC
  i=3
  if u3channels_savedC[i] == 'din':
    return d.getDIState(16+i)==1
  else:
    print "Error trying to get digital data from CIO"+str(i)+".  You didn't set it up for digital input."
    print "din"+str(i)+" exiting.  Bye bye."
    raise RuntimeError('Sorry...')
################################## DIGITAL OUTPUT CIO ################################
def doutC0(d,True_or_False = False):
  global u3channels_savedC
  i=0
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedC[i] == 'dout':
    d.setFIOState(16+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to CIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def doutC1(d,True_or_False = False):
  global u3channels_savedC
  i=1
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedC[i] == 'dout':
    d.setFIOState(16+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to CIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def doutC2(d,True_or_False = False):
  global u3channels_savedC
  i=2
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedC[i] == 'dout':
    d.setFIOState(16+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to CIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()
def doutC3(d,True_or_False = False):
  global u3channels_savedC
  i=3
  if True_or_False:
    zero_or_one=1
  else:
    zero_or_one=0
  if u3channels_savedC[i] == 'dout':
    d.setFIOState(16+i, state = zero_or_one)
  else:
    print "Error trying to send digital data to CIO"+str(i)+".  You didn't set it up for digital output."
    print "dout"+str(i)+" exiting.  Bye bye."
    raise RuntimeError()