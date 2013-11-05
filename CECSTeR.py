# CECSTeR - Consumer Electronics Control Security Testing Resource
#
# by Andy Davis (andy.davis@nccgroup.com)
#
# Release History:
#
# 18 April 2012 - v0.1 - First alpha release
# 02 May 2012 - v0.1b - First internal release
# 07 September 2012 - v1.0 - First public release


#!/usr/bin/python
import wx
import usb.core
import usb.util
import sys
import time
import string
import serial
import time
import os
from random import randint 
import wx.lib.agw.advancedsplash as AS

USE_GENERIC = 0

if USE_GENERIC:
    from wx.lib.stattext import GenStaticText as StaticText
else:
    StaticText = wx.StaticText
    
class MainPanel(wx.Panel):
    def __init__(self, parent, frame=None):
        wx.Panel.__init__(
            self, parent, -1,
            style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN|wx.NO_FULL_REPAINT_ON_RESIZE
            )


	if (len(sys.argv)!=2):
		print "\n-----------------------------------------------"
		print "Usage: CECSTeR <COM port>" 
		print "-----------------------------------------------\n"
		self.Close(True)
		sys.exit(0)

	self.serialport = int(sys.argv[1]) -1

        self.parent = parent
        self.frame = frame
                    
        self.SetBackgroundColour("White")
        self.Refresh()

	self.inputbufferlist = []

	self.dataview = True
	self.fuzzing = False
	self.capture = False
	self.opcode = ""
	self.source = "4"
	self.sourcename = "4 - Playback 1"
	self.target = "0"
	self.targetname = "0 - TV"
	self.physical = ""
	self.command_data = ""
	self.CurrentCommand = ""
	self.CurrentOpcode = ""
	self.parameters_required = ""	

	self.cdc_opcode = ""
	self.cdc_parameters_required = ""
	self.cdc_commandmode = False

	self.commandmode = False
	self.enumerating = False
	self.current_font_size = 12
	self.suppress_polling_messages = True
	self.fuzz_long_strings = False
	self.fuzz_format_strings = False
	self.fuzz_bit_flipping = False	
        
# create IDs   
     
	self.ID_About = wx.NewId()

	self.ID_Enumerate_Devices = wx.NewId()

	self.ID_Select_Device_Menu = wx.NewId()
	self.ID_0_TV = wx.NewId()
	self.ID_Recorder_1 = wx.NewId()
	self.ID_Recorder_2 = wx.NewId()
	self.ID_Tuner_1 = wx.NewId()
	self.ID_Playback_1 = wx.NewId()
	self.ID_Audio_System = wx.NewId()
	self.ID_Tuner_2 = wx.NewId()
	self.ID_Tuner_3 = wx.NewId()
	self.ID_Playback_2 = wx.NewId()
	self.ID_Recorder_3 = wx.NewId()
	self.ID_Tuner_4 = wx.NewId()
	self.ID_Playback_3 = wx.NewId()
	self.ID_Reserved_1 = wx.NewId()
	self.ID_Reserved_2 = wx.NewId()
	self.ID_Free_use = wx.NewId()
	self.ID_Broadcast = wx.NewId()

	self.ID_S_Select_Device_Menu = wx.NewId()
	self.ID_S_0_TV = wx.NewId()
	self.ID_S_Recorder_1 = wx.NewId()
	self.ID_S_Recorder_2 = wx.NewId()
	self.ID_S_Tuner_1 = wx.NewId()
	self.ID_S_Playback_1 = wx.NewId()
	self.ID_S_Audio_System = wx.NewId()
	self.ID_S_Tuner_2 = wx.NewId()
	self.ID_S_Tuner_3 = wx.NewId()
	self.ID_S_Playback_2 = wx.NewId()
	self.ID_S_Recorder_3 = wx.NewId()
	self.ID_S_Tuner_4 = wx.NewId()
	self.ID_S_Playback_3 = wx.NewId()
	self.ID_S_Reserved_1 = wx.NewId()
	self.ID_S_Reserved_2 = wx.NewId()
	self.ID_S_Free_use = wx.NewId()
	self.ID_S_Broadcast = wx.NewId()

	self.ID_One_Touch_Play_Menu = wx.NewId()
	self.ID_Active_Source = wx.NewId()
	self.ID_Image_View_On = wx.NewId()
	self.ID_Text_View_On = wx.NewId()

	self.ID_Routing_Control_Menu = wx.NewId()
	self.ID_Inactive_Source = wx.NewId()
	self.ID_Request_Active_Source = wx.NewId()
	self.ID_Routing_Change = wx.NewId()
	self.ID_Routing_Information = wx.NewId()
	self.ID_Set_Stream_Path = wx.NewId()

	self.ID_Standby_Menu = wx.NewId() 
	self.ID_Standby = wx.NewId() 	           

	self.ID_One_Touch_Record_Menu = wx.NewId()
	self.ID_Record_Off = wx.NewId()
	self.ID_Record_On = wx.NewId()
	self.ID_Record_Status = wx.NewId()
	self.ID_Record_TV_Screen = wx.NewId()

	self.ID_Timer_Programming_Menu = wx.NewId()
	self.ID_Clear_Analogue_Timer = wx.NewId()
	self.ID_Clear_Digital_Timer = wx.NewId()
	self.ID_Clear_External_Timer = wx.NewId()
	self.ID_Set_Analogue_Timer = wx.NewId()
	self.ID_Set_Digital_Timer = wx.NewId()
	self.ID_Set_External_Timer = wx.NewId()
	self.ID_Set_Timer_Programme_Title = wx.NewId()
	self.ID_Timer_Cleared_Status = wx.NewId()
	self.ID_Timer_Status = wx.NewId()

	self.ID_System_Information_Menu = wx.NewId()
	self.ID_CEC_Version = wx.NewId()
	self.ID_Get_CEC_Version = wx.NewId()
	self.ID_Give_Physical_Address = wx.NewId()
	self.ID_Get_Menu_Language = wx.NewId()
	self.ID_Report_Physical_Address = wx.NewId()
	self.ID_Set_Menu_Language = wx.NewId()

	self.ID_Deck_Control_Menu = wx.NewId()
	self.ID_Deck_Control = wx.NewId()
	self.ID_Deck_Status = wx.NewId()
	self.ID_Give_Deck_Status = wx.NewId()
	self.ID_Play = wx.NewId()

	self.ID_Tuner_Control_Menu = wx.NewId()
	self.ID_Give_Tuner_Device_Status = wx.NewId()
	self.ID_Select_Analogue_Service = wx.NewId()
	self.ID_Select_Digital_Service = wx.NewId()
	self.ID_Tuner_Device_Status = wx.NewId()
	self.ID_Tuner_Step_Decrement = wx.NewId()
	self.ID_Tuner_Step_Increment = wx.NewId()

	self.ID_Vendor_Specific_Commands_Menu = wx.NewId()
	self.ID_Device_Vendor_ID = wx.NewId()
	self.ID_Give_Device_Vendor_ID = wx.NewId()
	self.ID_Vendor_Command = wx.NewId()
	self.ID_Vendor_Command_With_ID = wx.NewId()
	self.ID_Vendor_Remote_Button_Down = wx.NewId()
	self.ID_Vendor_Remote_Button_Up = wx.NewId()

	self.ID_OSD_Display_Menu = wx.NewId()
	self.ID_Set_OSD_String = wx.NewId()

	self.ID_Device_OSD_Transfer_Menu = wx.NewId()
	self.ID_Give_OSD_Name = wx.NewId()
	self.ID_Set_OSD_Name = wx.NewId()

	self.ID_Device_Menu_Control_Menu = wx.NewId()
	self.ID_Menu_Request = wx.NewId()
	self.ID_Menu_Status = wx.NewId()
	self.ID_User_Control_Pressed = wx.NewId()
	self.ID_User_Control_Released = wx.NewId()

	self.ID_Remote_Control_Passthrough_Menu = wx.NewId()

	self.ID_Power_Status_Menu = wx.NewId()
	self.ID_Give_Device_Power_Status = wx.NewId()
	self.ID_Report_Power_Status = wx.NewId()

	self.ID_General_Protocol_Messages_Menu = wx.NewId()
	self.ID_Feature_Abort = wx.NewId()
	self.ID_Abort = wx.NewId()

	self.ID_System_Audio_Control_Menu = wx.NewId()
	self.ID_Give_Audio_Status = wx.NewId()
	self.ID_Give_System_Audio_Mode_Status = wx.NewId()
	self.ID_Report_Audio_Status = wx.NewId()
	self.ID_Report_Short_Audio_Descriptor = wx.NewId()
	self.ID_Request_Short_Audio_Descriptor = wx.NewId()
	self.ID_Set_System_Audio_Mode = wx.NewId()
	self.ID_System_Audio_Mode_Request = wx.NewId()
	self.ID_System_Audio_Mode_Status = wx.NewId()

	self.ID_Audio_Rate_Control_Menu = wx.NewId()
	self.ID_Set_Audio_Rate = wx.NewId()

	self.ID_Audio_Return_Channel_Control_Menu = wx.NewId()
	self.ID_Initiate_ARC = wx.NewId()
	self.ID_Report_ARC_Initiated = wx.NewId()
	self.ID_Report_ARC_Terminated = wx.NewId()
	self.ID_Request_ARC_Initiation = wx.NewId()
	self.ID_Request_ARC_Termination = wx.NewId()
	self.ID_Terminate_ARC = wx.NewId()

	self.ID_Capability_Discovery_And_Control_Menu = wx.NewId()
	self.ID_CDC_Message = wx.NewId()

	self.ID_HDMI_Ethernet_Channel_Menu = wx.NewId()
	self.ID_CDC_HEC_InquireState = wx.NewId()
	self.ID_CDC_HEC_ReportState = wx.NewId()
	self.ID_CDC_HEC_SetStateAdjacent = wx.NewId()
	self.ID_CDC_HEC_SetState = wx.NewId()
	self.ID_CDC_HEC_RequestDeactivation = wx.NewId()
	self.ID_CDC_HEC_NotifyAlive = wx.NewId()
	self.ID_CDC_HEC_Discover = wx.NewId()

	self.ID_CDC_HPD_Menu = wx.NewId()
	self.ID_CDC_HPD_SetState = wx.NewId()
	self.ID_CDC_HPD_ReportState = wx.NewId()

	self.ID_Fuzz_CEC = wx.NewId()
	self.ID_Fuzz_CDC = wx.NewId()
	self.ID_stop_fuzzing = wx.NewId()

	self.ID_Fuzzing_Config_Menu = wx.NewId()

	self.ID_Long_Strings = wx.NewId()
	self.ID_Format_Strings = wx.NewId()
	self.ID_Bit_Flipping = wx.NewId()

	self.ID_startcapture = wx.NewId()
	self.ID_stopcapture = wx.NewId()

	self.ID_showpollingmessages = wx.NewId()
	self.ID_showrawdata = wx.NewId()


# Splash screen

	pn = os.path.normpath(os.path.join(".", "images/cecster_splash.png"))
	bitmap = wx.Bitmap(pn, wx.BITMAP_TYPE_PNG)
	shadow = wx.WHITE
	frame = AS.AdvancedSplash(self, bitmap=bitmap, timeout=4000)
 
# create menu
        
        self.mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(self.ID_About, "&About")       

        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "Exit")

        self.mb.Append(file_menu, "File")

#-------------------------------------------------------------------------------------------------------------

        device_menu = wx.Menu()

        device_menu.Append(self.ID_Enumerate_Devices, "Enumerate Devices")   


	select_source_device_menu = wx.Menu()

	select_source_device_menu.Append(self.ID_S_0_TV, "0 - TV", "0 - TV", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Recorder_1, "1 - Recorder 1", "1 - Recorder 1", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Recorder_2, "2 - Recorder 2", "2 - Recorder 2", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Tuner_1, "3 - Tuner 1", "3 - Tuner 1", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Playback_1, "4 - Playback 1", "4 - Playback 1", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Audio_System, "5 - Audio System", "5 - Audio System", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Tuner_2, "6 - Tuner 2", "6 - Tuner 2", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Tuner_3, "7 - Tuner 3", "7 - Tuner 3", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Playback_2, "8 - Playback 2", "8 - Playback 2", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Recorder_3, "9 - Recorder 3", "9 - Recorder 3", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Tuner_4, "A - Tuner 4", "A - Tuner 4", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Playback_3, "B - Playback 3", "B - Playback 3", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Reserved_1, "C - Reserved 1", "C - Reserved 1", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Reserved_2, "D - Reserved 2", "D - Reserved 2", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Free_use, "E - Free use", "E - Free use", wx.ITEM_RADIO)
	select_source_device_menu.Append(self.ID_S_Broadcast, "F - Broadcast", "F - Broadcast", wx.ITEM_RADIO)

	device_menu.AppendMenu(self.ID_S_Select_Device_Menu, "Select Source Device", select_source_device_menu)

	select_device_menu = wx.Menu()

	select_device_menu.Append(self.ID_0_TV, "0 - TV", "0 - TV", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Recorder_1, "1 - Recorder 1", "1 - Recorder 1", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Recorder_2, "2 - Recorder 2", "2 - Recorder 2", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Tuner_1, "3 - Tuner 1", "3 - Tuner 1", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Playback_1, "4 - Playback 1", "4 - Playback 1", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Audio_System, "5 - Audio System", "5 - Audio System", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Tuner_2, "6 - Tuner 2", "6 - Tuner 2", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Tuner_3, "7 - Tuner 3", "7 - Tuner 3", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Playback_2, "8 - Playback 2", "8 - Playback 2", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Recorder_3, "9 - Recorder 3", "9 - Recorder 3", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Tuner_4, "A - Tuner 4", "A - Tuner 4", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Playback_3, "B - Playback 3", "B - Playback 3", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Reserved_1, "C - Reserved 1", "C - Reserved 1", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Reserved_2, "D - Reserved 2", "D - Reserved 2", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Free_use, "E - Free use", "E - Free use", wx.ITEM_RADIO)
	select_device_menu.Append(self.ID_Broadcast, "F - Broadcast", "F - Broadcast", wx.ITEM_RADIO)

	device_menu.AppendMenu(self.ID_Select_Device_Menu, "Select Target Device", select_device_menu)

        self.mb.Append(device_menu, "Device")

#-------------------------------------------------------------------------------------------------------------

	command_menu = wx.Menu()

	one_touch_play_menu = wx.Menu()

	one_touch_play_menu.Append(self.ID_Active_Source, "Active Source")
	one_touch_play_menu.Append(self.ID_Image_View_On, "Image View On")
	one_touch_play_menu.Append(self.ID_Text_View_On, "Text View On")

	command_menu.AppendMenu(self.ID_One_Touch_Play_Menu, "One Touch Play", one_touch_play_menu)

#-------------------------------------------------------------------------------------------------------------

	routing_control_menu = wx.Menu()


	routing_control_menu.Append(self.ID_Active_Source, "Active Source")
	routing_control_menu.Append(self.ID_Inactive_Source, "Inactive Source")
	routing_control_menu.Append(self.ID_Request_Active_Source, "Request Active Source")
	routing_control_menu.Append(self.ID_Routing_Change, "Routing Change")
	routing_control_menu.Append(self.ID_Routing_Information, "Routing Information")
	routing_control_menu.Append(self.ID_Set_Stream_Path, "Set Stream Path")

	command_menu.AppendMenu(self.ID_Routing_Control_Menu, "Routing Control", routing_control_menu)

#-------------------------------------------------------------------------------------------------------------

	standby_menu = wx.Menu()

	standby_menu.Append(self.ID_Standby, "Standby")

	command_menu.AppendMenu(self.ID_Standby_Menu, "Standby", standby_menu)

#-------------------------------------------------------------------------------------------------------------

	one_touch_record_menu = wx.Menu()

	one_touch_record_menu.Append(self.ID_Record_Off, "Record Off")
	one_touch_record_menu.Append(self.ID_Record_On, "Record On")
	one_touch_record_menu.Append(self.ID_Record_Status, "Record Status")
	one_touch_record_menu.Append(self.ID_Record_TV_Screen, "Record TV Screen")

	command_menu.AppendMenu(self.ID_One_Touch_Record_Menu, "One Touch Record", one_touch_record_menu)

#-------------------------------------------------------------------------------------------------------------

	timer_programming_menu = wx.Menu()

	timer_programming_menu.Append(self.ID_Clear_Analogue_Timer, "Clear Analogue Timer")
	timer_programming_menu.Append(self.ID_Clear_Digital_Timer, "Clear Digital Timer")
	timer_programming_menu.Append(self.ID_Clear_External_Timer, "Clear External Timer")
	timer_programming_menu.Append(self.ID_Set_Analogue_Timer, "Set Analogue Timer")
	timer_programming_menu.Append(self.ID_Set_Digital_Timer, "Set Digital Timer")
	timer_programming_menu.Append(self.ID_Set_External_Timer, "Set External Timer")
	timer_programming_menu.Append(self.ID_Set_Timer_Programme_Title, "Set Timer Programme Title")
	timer_programming_menu.Append(self.ID_Timer_Cleared_Status, "Timer Cleared Status")
	timer_programming_menu.Append(self.ID_Timer_Status, "Timer Status")


	command_menu.AppendMenu(self.ID_Timer_Programming_Menu, "Timer Programming", timer_programming_menu)

#-------------------------------------------------------------------------------------------------------------

	system_information_menu = wx.Menu()

	system_information_menu.Append(self.ID_CEC_Version, "CEC Version")
	system_information_menu.Append(self.ID_Get_CEC_Version, "Get CEC Version")
	system_information_menu.Append(self.ID_Give_Physical_Address, "Give Physical Address")
	system_information_menu.Append(self.ID_Get_Menu_Language, "Get Menu Language")
	system_information_menu.Append(self.ID_Report_Physical_Address, "Report Physical Address")
	system_information_menu.Append(self.ID_Set_Menu_Language, "Set Menu Language")

	command_menu.AppendMenu(self.ID_System_Information_Menu, "System Information", system_information_menu)

#-------------------------------------------------------------------------------------------------------------

	deck_control_menu = wx.Menu()

	deck_control_menu.Append(self.ID_Deck_Control, "Deck Control")
	deck_control_menu.Append(self.ID_Deck_Status, "Deck Status")
	deck_control_menu.Append(self.ID_Give_Deck_Status, "Give Deck Status")
	deck_control_menu.Append(self.ID_Play, "Play")

	command_menu.AppendMenu(self.ID_Deck_Control_Menu, "Deck Control", deck_control_menu)

#-------------------------------------------------------------------------------------------------------------

	tuner_control_menu = wx.Menu()

	tuner_control_menu.Append(self.ID_Give_Tuner_Device_Status, "Give Tuner Device Status")
	tuner_control_menu.Append(self.ID_Select_Analogue_Service, "Select Analogue Service")
	tuner_control_menu.Append(self.ID_Select_Digital_Service, "Select Digital Service")
	tuner_control_menu.Append(self.ID_Tuner_Device_Status, "Tuner Device Status")
	tuner_control_menu.Append(self.ID_Tuner_Step_Decrement, "Tuner Step Decrement")
	tuner_control_menu.Append(self.ID_Tuner_Step_Increment, "Tuner Step Increment")

	command_menu.AppendMenu(self.ID_Tuner_Control_Menu, "Tuner Control", tuner_control_menu)

#-------------------------------------------------------------------------------------------------------------

	vendor_specific_commands_menu = wx.Menu()

	vendor_specific_commands_menu.Append(self.ID_CEC_Version, "CEC Version")
	vendor_specific_commands_menu.Append(self.ID_Device_Vendor_ID, "Device Vendor ID")
	vendor_specific_commands_menu.Append(self.ID_Get_CEC_Version, "Get CEC Version")
	vendor_specific_commands_menu.Append(self.ID_Give_Device_Vendor_ID, "Give Device Vendor ID")
	vendor_specific_commands_menu.Append(self.ID_Vendor_Command, "Vendor Command")
	vendor_specific_commands_menu.Append(self.ID_Vendor_Command_With_ID, "Vendor Command With ID")
	vendor_specific_commands_menu.Append(self.ID_Vendor_Remote_Button_Down, "Vendor Remote Button Down")
	vendor_specific_commands_menu.Append(self.ID_Vendor_Remote_Button_Up, "Vendor Remote Button Up")

	command_menu.AppendMenu(self.ID_Vendor_Specific_Commands_Menu, "Vendor Specific Commands", vendor_specific_commands_menu)

#-------------------------------------------------------------------------------------------------------------

	OSD_display_menu = wx.Menu()

	OSD_display_menu.Append(self.ID_Set_OSD_String, "Set OSD String")

	command_menu.AppendMenu(self.ID_OSD_Display_Menu, "OSD Display", OSD_display_menu)

#-------------------------------------------------------------------------------------------------------------

	device_OSD_transfer_menu = wx.Menu()

	device_OSD_transfer_menu.Append(self.ID_Give_OSD_Name, "Give OSD Name")
	device_OSD_transfer_menu.Append(self.ID_Set_OSD_Name, "Set OSD Name")

	command_menu.AppendMenu(self.ID_Device_OSD_Transfer_Menu, "Device OSD Transfer", device_OSD_transfer_menu)

#-------------------------------------------------------------------------------------------------------------

	device_menu_control_menu = wx.Menu()

	device_menu_control_menu.Append(self.ID_Menu_Request, "Menu Request")
	device_menu_control_menu.Append(self.ID_Menu_Status, "Menu Status")
	device_menu_control_menu.Append(self.ID_User_Control_Pressed, "User Control Pressed")
	device_menu_control_menu.Append(self.ID_User_Control_Released, "User Control Released")

	command_menu.AppendMenu(self.ID_Device_Menu_Control_Menu, "Device Menu Control", device_menu_control_menu)

#-------------------------------------------------------------------------------------------------------------

	remote_control_passthrough_menu = wx.Menu()

	remote_control_passthrough_menu.Append(self.ID_User_Control_Pressed, "User Control Pressed")
	remote_control_passthrough_menu.Append(self.ID_User_Control_Released, "User Control Released")

	command_menu.AppendMenu(self.ID_Remote_Control_Passthrough_Menu, "Remote Control Passthrough", remote_control_passthrough_menu)

#-------------------------------------------------------------------------------------------------------------

	power_status_menu = wx.Menu()

	power_status_menu.Append(self.ID_Give_Device_Power_Status, "Give Device Power Status")
	power_status_menu.Append(self.ID_Report_Power_Status, "Report Power Status")

	command_menu.AppendMenu(self.ID_Power_Status_Menu, "Power Status", power_status_menu)

#-------------------------------------------------------------------------------------------------------------

	general_protocol_messages_menu = wx.Menu()

	general_protocol_messages_menu.Append(self.ID_Feature_Abort, "Feature Abort")
	general_protocol_messages_menu.Append(self.ID_Abort, "Abort")

	command_menu.AppendMenu(self.ID_General_Protocol_Messages_Menu, "General Protocol Messages", general_protocol_messages_menu)

#-------------------------------------------------------------------------------------------------------------

	system_audio_control_menu = wx.Menu()

	system_audio_control_menu.Append(self.ID_Give_Audio_Status, "Give Audio Status")
	system_audio_control_menu.Append(self.ID_Give_System_Audio_Mode_Status, "Give System Audio Mode Status")
	system_audio_control_menu.Append(self.ID_Report_Audio_Status, "Report Audio Status")
	system_audio_control_menu.Append(self.ID_Report_Short_Audio_Descriptor, "Report Short Audio Descriptor")
	system_audio_control_menu.Append(self.ID_Request_Short_Audio_Descriptor, "Request Short Audio Descriptor")
	system_audio_control_menu.Append(self.ID_Set_System_Audio_Mode, "Set System Audio Mode")
	system_audio_control_menu.Append(self.ID_System_Audio_Mode_Request, "System Audio Mode Request")
	system_audio_control_menu.Append(self.ID_System_Audio_Mode_Status, "System Audio Mode Status")
	system_audio_control_menu.Append(self.ID_User_Control_Pressed, "User Control Pressed")
	system_audio_control_menu.Append(self.ID_User_Control_Released, "User Control Released")

	command_menu.AppendMenu(self.ID_System_Audio_Control_Menu, "System Audio Control", system_audio_control_menu)

#-------------------------------------------------------------------------------------------------------------

	audio_rate_control_menu = wx.Menu()

	audio_rate_control_menu.Append(self.ID_Set_Audio_Rate, "Set Audio Rate")

	command_menu.AppendMenu(self.ID_Audio_Rate_Control_Menu, "Audio Rate Control", audio_rate_control_menu)

#-------------------------------------------------------------------------------------------------------------

	audio_return_channel_control_menu = wx.Menu()

	audio_return_channel_control_menu.Append(self.ID_Initiate_ARC, "Initiate ARC")
	audio_return_channel_control_menu.Append(self.ID_Report_ARC_Initiated, "Report ARC Initiated")
	audio_return_channel_control_menu.Append(self.ID_Report_ARC_Terminated, "Report ARC Terminated")
	audio_return_channel_control_menu.Append(self.ID_Request_ARC_Initiation, "Request ARC Initiation")
	audio_return_channel_control_menu.Append(self.ID_Request_ARC_Termination, "Request ARC Termination")
	audio_return_channel_control_menu.Append(self.ID_Terminate_ARC, "Terminate ARC")

	command_menu.AppendMenu(self.ID_Audio_Return_Channel_Control_Menu, "Audio Return Channel Control", audio_return_channel_control_menu)

#-------------------------------------------------------------------------------------------------------------

	capability_discovery_and_control_menu = wx.Menu()

	capability_discovery_and_control_menu.Append(self.ID_CDC_Message, "CDC Message")

	command_menu.AppendMenu(self.ID_Capability_Discovery_And_Control_Menu, "Capability Discovery and Control", capability_discovery_and_control_menu)

#-------------------------------------------------------------------------------------------------------------

	self.mb.Append(command_menu, "CEC Features")

#-------------------------------------------------------------------------------------------------------------

	cdc_command_menu = wx.Menu()

	hdmi_ethernet_channel_menu = wx.Menu()

	hdmi_ethernet_channel_menu.Append(self.ID_CDC_HEC_InquireState, "CDC HEC InquireState")
	hdmi_ethernet_channel_menu.Append(self.ID_CDC_HEC_ReportState, "CDC HEC ReportState")
	hdmi_ethernet_channel_menu.Append(self.ID_CDC_HEC_SetStateAdjacent, "CDC HEC SetStateAdjacent")
	hdmi_ethernet_channel_menu.Append(self.ID_CDC_HEC_SetState, "CDC HEC SetState")
	hdmi_ethernet_channel_menu.Append(self.ID_CDC_HEC_RequestDeactivation, "CDC HEC RequestDeactivation")
	hdmi_ethernet_channel_menu.Append(self.ID_CDC_HEC_NotifyAlive, "CDC HEC NotifyAlive")
	hdmi_ethernet_channel_menu.Append(self.ID_CDC_HEC_Discover, "CDC HEC Discover")

	cdc_command_menu.AppendMenu(self.ID_HDMI_Ethernet_Channel_Menu, "HDMI Ethernet Channel", hdmi_ethernet_channel_menu)

#-------------------------------------------------------------------------------------------------------------

	cdc_hpd_menu = wx.Menu()

	cdc_hpd_menu.Append(self.ID_CDC_HPD_SetState, "CDC HPD SetState")
	cdc_hpd_menu.Append(self.ID_CDC_HPD_ReportState, "CDC HPD ReportState")

	cdc_command_menu.AppendMenu(self.ID_CDC_HPD_Menu, "CDC HPD", cdc_hpd_menu)

#-------------------------------------------------------------------------------------------------------------

	self.mb.Append(cdc_command_menu, "CDC Features")

#-------------------------------------------------------------------------------------------------------------

        fuzzing_menu = wx.Menu()

	fuzzing_config_menu = wx.Menu()

	fuzzing_config_menu.Append(self.ID_Long_Strings, "Long Strings", "Long Strings", wx.ITEM_CHECK)
	fuzzing_config_menu.Append(self.ID_Format_Strings, "Format Strings", "Format Strings", wx.ITEM_CHECK)
	fuzzing_config_menu.Append(self.ID_Bit_Flipping, "Bit Flipping", "Bit Flipping", wx.ITEM_CHECK)

	fuzzing_menu.AppendMenu(self.ID_Fuzzing_Config_Menu, "Fuzzing Config", fuzzing_config_menu)

        fuzzing_menu.Append(self.ID_Fuzz_CEC, "Fuzz CEC")   
        fuzzing_menu.Append(self.ID_stop_fuzzing, "Stop Fuzzing") 

        self.mb.Append(fuzzing_menu, "Fuzzing")

#-------------------------------------------------------------------------------------------------------------

        capture_menu = wx.Menu()

        capture_menu.Append(self.ID_startcapture, "Start CEC Capture")   
        capture_menu.Append(self.ID_stopcapture, "Stop CEC Capture")      
       
        self.mb.Append(capture_menu, "Capture")

#-------------------------------------------------------------------------------------------------------------

        view_menu = wx.Menu()

        view_menu.Append(self.ID_showpollingmessages, "Show Polling Messages", "Show polling messages",wx.ITEM_CHECK)   
        view_menu.Append(self.ID_showrawdata, "Suppress Raw Data","show raw data", wx.ITEM_CHECK)      
       
        self.mb.Append(view_menu, "View")

#-------------------------------------------------------------------------------------------------------------

        self.parent.SetMenuBar(self.mb)

#-------------------------------------------------------------------------------------------------------------


	# "Command name", "Opcode", "parameters expected?" 

	self.command_list = [
	["Active Source", "82",1],
	["Image View On", "04",0],
	["Text View On", "0D",0],

	["Inactive Source", "9D",1],
	["Request Active Source", "85",0],
	["Routing Change", "80",1],
	["Routing Information", "81",1],
	["Set Stream Path", "86",1],

	["Standby", "36",0],

	["Record Off", "0B",0],
	["Record On", "09",1],
	["Record Status", "0A",1],
	["Record TV Screen", "0F",0],

	["Clear Analogue Timer", "33",1],
	["Clear Digital Timer", "99",1],
	["Clear External Timer", "A1",1],
	["Set Analogue Timer", "34",1],
	["Set Digital Timer", "97",1],
	["Set External Timer", "A2",1],
	["Set Timer Programme Title", "67",1],
	["Timer Cleared Status", "43",1],
	["Timer Status", "35",1],

	["CEC Version", "9E",1],
	["Get CEC Version", "9F",0],
	["Give Physical Address", "83",0],
	["Get Menu Language", "91",0],
	["Report Physical Address", "84",1],
	["Set Menu Language", "32",1],

	["Deck Control", "42",1],
	["Deck Status", "1B",1],
	["Give Deck Status", "1A",1],
	["Play", "41",1],

	["Give Tuner Device Status", "08",1],
	["Select Analogue Service", "92",1],
	["Select Digital Service", "93",1],
	["Tuner Device Status", "07",1],
	["Tuner Step Decrement", "06",0],
	["Tuner Step Increment", "05",0],

	["Device Vendor ID", "87",1],
	["Give Device Vendor ID", "8C",0],
	["Vendor Command", "89",1],
	["Vendor Command With ID", "A0",1],
	["Vendor Remote Button Down", "8A",1],
	["Vendor Remote Button Up", "8B",1],

	["Set OSD String", "64",1],

	["Give OSD Name", "46",0],
	["Set OSD Name", "47",1],

	["Menu Request", "8D",1],
	["Menu Status", "8E",1],
	["User Control Pressed", "44",1],
	["User Control Released", "45",1],

	["Give Device Power Status", "8F",0],
	["Report Power Status", "90",1],

	["Feature Abort", "00",1],
	["Abort", "FF",0],

	["Give Audio Status", "71",0],
	["Give System Audio Mode Status", "7E",0],
	["Report Audio Status", "7A",1],
	["Report Short Audio Descriptor", "A3",1],
	["Request Short Audio Descriptor", "A4",1],
	["Set System Audio Mode", "72",1],
	["System Audio Mode Request", "70",1],
	["System Audio Mode Status", "7E",1],

	["Set Audio Rate", "9A",1],

	["Initiate ARC", "C0",0],
	["Report ARC Initiated", "C1",0],
	["Report ARC Terminated", "C2",0],
	["Request ARC Initiation", "C3",0],
	["Request ARC Termination", "C4",0],
	["Terminate ARC", "C5",0],

	["CDC Message", "F8",1]]


	self.cdc_command_list = [
	["CDC HEC InquireState", "00",1],
	["CDC HEC ReportState", "01",1],
	["CDC HEC SetStateAdjacent", "02",1],
	["CDC HEC SetState", "03",1],
	["CDC HEC RequestDeactivation", "04",1],
	["CDC HEC NotifyAlive", "05",0],
	["CDC HEC Discover", "06",0],

	["CDC HPD SetState", "10",1],
	["CDC HPD ReportState", "11",1]]




	self.target_list = [
	["0 - TV", "0"],
	["1 - Recorder 1","1"],
	["2 - Recorder 2","2"],
	["3 - Tuner 1","3"],
	["4 - Playback 1","4"],
	["5 - Audio System","5"],
	["6 - Tuner 2","6"],
	["7 - Tuner 3","7"],
	["8 - Playback 2","8"],
	["9 - Recorder 3","9"],
	["A - Tuner 4","A"],
	["B - Playback 3","B"],
	["C - Reserved 1","C"],
	["D - Reserved 2","D"],
	["E - Free use","E"],
	["F - Broadcast","F"]]


	self.source_list = [
	["0 - TV", "0"],
	["1 - Recorder 1","1"],
	["2 - Recorder 2","2"],
	["3 - Tuner 1","3"],
	["4 - Playback 1","4"],
	["5 - Audio System","5"],
	["6 - Tuner 2","6"],
	["7 - Tuner 3","7"],
	["8 - Playback 2","8"],
	["9 - Recorder 3","9"],
	["A - Tuner 4","A"],
	["B - Playback 3","B"],
	["C - Reserved 1","C"],
	["D - Reserved 2","D"],
	["E - Free use","E"],
	["F - Broadcast","F"]]


	self.vendorid_list = [
	["samsung", "00 00 F0"],
	["LG", "00 E0 91"],
	["Panasonic", "00 80 45"],
	["Pioneer", "00 E0 36"],
	["Onkyo", "00 09 B0"],
	["Yamaha", "00 A0 DE"],
	["Philips", "00 90 3E"],
	["Sony", "08 00 46"],
	["Toshiba", "00 00 39"]]

                
# Create status bar

        self.statusbar = self.parent.CreateStatusBar(4, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-1,-1,-1,-1])
        self.statusbar.SetStatusText("", 0)
	status1 = "Source Device: " + self.sourcename
	status2 = "Target Device: " + self.targetname
        self.statusbar.SetStatusText(status1, 1) 
	self.statusbar.SetStatusText(status2, 2)
        self.statusbar.SetStatusText("Status: Normal", 3)                
        
# Background images        
        
        image_file = 'images/cecster_logo.png'
        image = wx.Bitmap(image_file)
        image_size = image.GetSize()
        bm = wx.StaticBitmap(self, wx.ID_ANY, image, size=image_size, pos=(5,16))
        
        image_file = 'images/ncc_logo.png'
        image = wx.Bitmap(image_file)
        image_size = image.GetSize()
        bm = wx.StaticBitmap(self, wx.ID_ANY, image, size=image_size, pos=(840,3))

        image_file = 'images/underline.png'
        image = wx.Bitmap(image_file)
        image_size = image.GetSize()
        bm = wx.StaticBitmap(self, wx.ID_ANY, image, size=image_size, pos=(5,60))


# Text controls

        text = wx.StaticText(self, -1, "Output:",pos=(10,80))
        text.SetBackgroundColour('White')
        font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL)
        text.SetFont(font)

        self.output = wx.TextCtrl(self, -1,"",size=(985, 500), pos=(10, 100), style=wx.TE_MULTILINE|wx.TE_RICH2
|wx.TE_READONLY)
	self.output.SetBackgroundColour("BLACK")

        f = wx.Font(self.current_font_size, wx.MODERN, wx.NORMAL, wx.NORMAL)
	self.output.SetDefaultStyle(wx.TextAttr("GREEN", wx.NullColour, f))
	self.output.AppendText("Welcome to CECSTeR v1.0 - The Consumer Electronics Control Security Testing Resource\n")
	self.output.AppendText("The tool enables the testing of HDMI protocols including CEC, CDC and HEC\n\n")

        text = wx.StaticText(self, -1, "Commands:",pos=(10,605))
        text.SetBackgroundColour('White')
        font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL)
        text.SetFont(font)

        self.command = wx.TextCtrl(self, -1,"",size=(985, 60), pos=(10, 625), style=wx.TE_MULTILINE|wx.TE_RICH2)

	self.command.Bind(wx.EVT_KEY_DOWN, self.OnKey) 


	self.command.SetBackgroundColour("BLACK")

        f = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
	self.command.SetDefaultStyle(wx.TextAttr("GREEN", wx.NullColour, f))
	self.command.AppendText("CEC:> ")
	self.command.SetFocus()


	self.parent.Bind(wx.EVT_MENU, self.About, id=self.ID_About)
        self.parent.Bind(wx.EVT_MENU, self.CloseMe, id=wx.ID_EXIT)  

	self.parent.Bind(wx.EVT_MENU, self.EnumerateBus, id=self.ID_Enumerate_Devices)

	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_0_TV)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Recorder_1)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Recorder_2)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Tuner_1)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Playback_1)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Audio_System)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Tuner_2)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Tuner_3)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Playback_2)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Recorder_3)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Tuner_4)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Playback_3)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Reserved_1)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Reserved_2)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Free_use)
	self.parent.Bind(wx.EVT_MENU, self.ProcessSourceSelect, id=self.ID_S_Broadcast)

	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_0_TV)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Recorder_1)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Recorder_2)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Tuner_1)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Playback_1)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Audio_System)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Tuner_2)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Tuner_3)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Playback_2)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Recorder_3)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Tuner_4)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Playback_3)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Reserved_1)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Reserved_2)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Free_use)
	self.parent.Bind(wx.EVT_MENU, self.ProcessTargetSelect, id=self.ID_Broadcast)

	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Active_Source)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Image_View_On)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Text_View_On)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Inactive_Source)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Request_Active_Source)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Routing_Change)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Routing_Information)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Set_Stream_Path)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Standby) 	           
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Record_Off)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Record_On)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Record_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Record_TV_Screen)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Clear_Analogue_Timer)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Clear_Digital_Timer)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Clear_External_Timer)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Set_Analogue_Timer)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Set_Digital_Timer)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Set_External_Timer)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Set_Timer_Programme_Title)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Timer_Cleared_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Timer_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_CEC_Version)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Get_CEC_Version)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Give_Physical_Address)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Get_Menu_Language)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Report_Physical_Address)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Set_Menu_Language)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Deck_Control)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Deck_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Give_Deck_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Play)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Give_Tuner_Device_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Select_Analogue_Service)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Select_Digital_Service)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Tuner_Device_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Tuner_Step_Decrement)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Tuner_Step_Increment)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Device_Vendor_ID)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Give_Device_Vendor_ID)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Vendor_Command)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Vendor_Command_With_ID)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Vendor_Remote_Button_Down)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Vendor_Remote_Button_Up)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Set_OSD_String)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Give_OSD_Name)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Set_OSD_Name)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Menu_Request)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Menu_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_User_Control_Pressed)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_User_Control_Released)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Give_Device_Power_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Report_Power_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Feature_Abort)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Abort)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Give_Audio_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Give_System_Audio_Mode_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Report_Audio_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Report_Short_Audio_Descriptor)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Request_Short_Audio_Descriptor)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Set_System_Audio_Mode)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_System_Audio_Mode_Request)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_System_Audio_Mode_Status)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Set_Audio_Rate)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Initiate_ARC)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Report_ARC_Initiated)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Report_ARC_Terminated)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Request_ARC_Initiation)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Request_ARC_Termination)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_Terminate_ARC)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCommand, id=self.ID_CDC_Message)

	self.parent.Bind(wx.EVT_MENU, self.ProcessCDCCommand, id=self.ID_CDC_HEC_InquireState)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCDCCommand, id=self.ID_CDC_HEC_ReportState)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCDCCommand, id=self.ID_CDC_HEC_SetStateAdjacent)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCDCCommand, id=self.ID_CDC_HEC_SetState)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCDCCommand, id=self.ID_CDC_HEC_RequestDeactivation)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCDCCommand, id=self.ID_CDC_HEC_NotifyAlive)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCDCCommand, id=self.ID_CDC_HEC_Discover)

	self.parent.Bind(wx.EVT_MENU, self.ProcessCDCCommand, id=self.ID_CDC_HPD_SetState)
	self.parent.Bind(wx.EVT_MENU, self.ProcessCDCCommand, id=self.ID_CDC_HPD_ReportState)

	self.parent.Bind(wx.EVT_MENU, self.FuzzCEC, id=self.ID_Fuzz_CEC)
	self.parent.Bind(wx.EVT_MENU, self.StopFuzzing, id=self.ID_stop_fuzzing)

	self.parent.Bind(wx.EVT_MENU, self.Toggle_Long_Strings, id=self.ID_Long_Strings)
	self.parent.Bind(wx.EVT_MENU, self.Toggle_Format_Strings, id=self.ID_Format_Strings)
	self.parent.Bind(wx.EVT_MENU, self.Toggle_Bit_Flipping, id=self.ID_Bit_Flipping)

	self.parent.Bind(wx.EVT_MENU, self.Toggle_polling, id=self.ID_showpollingmessages)
	self.parent.Bind(wx.EVT_MENU, self.Toggle_dataview, id=self.ID_showrawdata)

	self.parent.Bind(wx.EVT_MENU, self.StartCapture, id=self.ID_startcapture)
	self.parent.Bind(wx.EVT_MENU, self.StopCapture, id=self.ID_stopcapture)

	

#------- main code -------------------------------------------------------------------------------------------

	try:
		self.ser = serial.Serial(self.serialport, 9600, timeout=0.5, parity=serial.PARITY_NONE, stopbits=1)

	except:
		wx.MessageBox("Serial communication error", caption="Error", style=wx.OK|wx.ICON_ERROR, parent=self)
		self.Close(True)
		sys.exit(0)

	
	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Status: CEC-USB Bridge connected ok\n")
	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	
		
	self.physical = self.GetPhysicalAddress()
	wx.Yield()
	self.source = self.GetLogicalAddress()
	wx.Yield()

	#command = "!OCECSTeR~"
	#self.RawCommandSend (command)

	self.output.AppendText("Status: Source configured as physical address: ")
	self.output.AppendText(self.physical[0])
	self.output.AppendText(".")
	self.output.AppendText(self.physical[1])
	self.output.AppendText(".")
	self.output.AppendText(self.physical[2])
	self.output.AppendText(".")
	self.output.AppendText(self.physical[3])
	self.output.AppendText("\n")
	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Status: Source configured as logical address: ")
	self.output.AppendText(self.sourcename)
	self.output.AppendText("\n")
	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Status: Target configured as logical address: ")
	self.output.AppendText(self.targetname)
	self.output.AppendText("\n")


#------- functions -------------------------------------------------------------------------------------------



    def RawCommandSend(self,CommandToSend):

	self.ser.write (CommandToSend)


    def SendCommand(self,target,opcode,data):

	command = "!x"
	command += target
	command += " "
	command += opcode
	command += " "
	command += data
	command += "~"

	if opcode == "":
		print "no opcode"
		return

	
	self.RawCommandSend (command)
	print command

	found = False
	x = 0
	while (x < len (self.command_list)):
		if (self.command_list[x][1] == opcode):
			self.CurrentCommand = self.command_list[x][0]
			found = True
			break
		x+=1

	if (found == False):
		self.CurrentCommand = "Unknown"

	if (self.enumerating == True):
		return command

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Sent command: ")
	self.output.AppendText(opcode)
	self.output.AppendText(" - \"")
	self.output.AppendText(self.CurrentCommand)
	self.output.AppendText("\"")
	self.output.AppendText("\n")	
	
	return command				



    def StartCapture(self,event):

	self.capture = True
	self.statusbar.SetStatusText("Status: Capturing", 3) 
	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Status: CEC capture started ")
	if (self.suppress_polling_messages == True):
		self.output.AppendText("(\"polling\" messages are being suppressed)\n")
	else:
		self.output.AppendText("\n")

	self.output.AppendText("\n")

	while (self.capture == True):
		wx.Yield()
		self.DisplayResponse()


    def StopCapture(self,event):

	if (self.capture == False):
		return

	self.capture = False
	self.output.AppendText("\n")
	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Status: CEC capture stopped\n")
	self.statusbar.SetStatusText("Status: Normal", 3) 
	self.output.AppendText("\n")		



    def GetPhysicalAddress(self):
	command = "!P~"

	self.RawCommandSend (command)
	sub = "PHY "
	self.enumerating = True		# prevent extraneous text being output by ReceiveData()
	buf = self.ReceiveData()
	self.enumerating = False
	pos = string.find(buf, sub)
	pos += 4
	physical =  buf[pos]
	physical += buf[pos+1]
	physical += buf[pos+2]
	physical += buf[pos+3]

	return physical


    def GetLogicalAddress(self):
	command = "!a~"

	self.RawCommandSend (command)
	sub = "ADR "
	self.enumerating = True		# prevent extraneous text being output by ReceiveData()
	buf = self.ReceiveData()
	self.enumerating = False
	pos = string.find(buf, sub)
	pos += 4
	logical = buf[pos]

	x = 0
	while (x < len (self.source_list)):
		if (self.source_list[x][1] == logical):
			self.sourcename = self.source_list[x][0]
		x+=1

	status = "Source Device: " + self.sourcename
        self.statusbar.SetStatusText(status, 1) 

	return logical

		
    def EnumerateBus(self,event):
	x = 0
	target = ""
	data = ""
	buf = ""
	sub = ""

	self.enumerating = True

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Status: Enumerating CEC bus - the following devices are present:")
	self.output.AppendText("\n\n")
	


	while (x < 16):

		wx.Yield()

		target = "%x" % x
		target = target.upper()
		alive = ""
		opcode = "FF"

		CommandSent = self.SendCommand(target,opcode,data)
		sub = "REC " + self.source + target + " FF"
		buf = self.ReceiveData()
		pos = string.find(buf, sub)
		pos += 10

		if buf[pos] == "1":

			y = 0
			while (y < len (self.target_list)):
				if target == self.target_list[y][1]:
					alive =  self.target_list[y][0]
					self.output.AppendText(alive)
					if (target == self.source):
						self.output.AppendText(" (CECSTeR)")

					self.output.AppendText("\n")
				y+=1
		
		x+=1

	self.output.AppendText("\n")
	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Status: Bus enumeration complete")
	self.output.AppendText("\n")
	self.enumerating = False


    def	Toggle_polling(self,event):

	if self.suppress_polling_messages == True:
		self.suppress_polling_messages = False
		self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
		self.output.AppendText("Status: Configuration changed - \"Polling messages\" enabled\n")
	else:
		self.suppress_polling_messages = True
		self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
		self.output.AppendText("Status: Configuration changed - \"Polling messages\" suppressed\n")


    def	Toggle_dataview(self,event):

	if self.dataview == True:
		self.dataview = False
		self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
		self.output.AppendText("Status: Configuration changed - \"Raw data\" suppressed\n")
	else:
		self.dataview = True
		self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
		self.output.AppendText("Status: Configuration changed - \"Raw data\" enabled\n")


    def	Toggle_Long_Strings(self,event):
	
	if self.fuzz_long_strings == True:
		self.fuzz_long_strings = False
		self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
		self.output.AppendText("Fuzzing: Configuration changed - \"Long Strings\" disabled\n")
	else:
		self.fuzz_long_strings = True
		self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
		self.output.AppendText("Fuzzing: Configuration changed - \"Long Strings\" enabled\n")


    def	Toggle_Format_Strings(self,event):

	if self.fuzz_format_strings == True:
		self.fuzz_format_strings = False
		self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
		self.output.AppendText("Fuzzing: Configuration changed - \"Format Strings\" disabled\n")
	else:
		self.fuzz_format_strings = True
		self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
		self.output.AppendText("Fuzzing: Configuration changed - \"Format Strings\" enabled\n")


    def	Toggle_Bit_Flipping(self,event):

	if self.fuzz_bit_flipping == True:
		self.fuzz_bit_flipping = False
		self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
		self.output.AppendText("Fuzzing: Configuration changed - \"Bit Flipping\" disabled\n")
	else:
		self.fuzz_bit_flipping = True
		self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
		self.output.AppendText("Fuzzing: Configuration changed - \"Bit Flipping\" enabled\n")



    def	FuzzCEC(self,event):


	logfilepath = "logfile_CEC_" + time.strftime("%Y-%m-%d", time.localtime()) + ".txt"
	self.fplog = file(logfilepath, 'a')	# open logfile for writing
	self.fplog.write("\n\n**** CECSTeR Log file ****\n\n")

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: CEC Fuzzer started\n")

	self.fplog.write(time.strftime("%H:%M:%S  ", time.localtime()))
	self.fplog.write("Fuzzing: CEC Fuzzer started\n")

	self.fuzzing = True
	self.statusbar.SetStatusText("Status: Fuzzing", 3)	


	if (self.fuzz_long_strings == True):
		self.TestCase1(0x00,0xff)

	if (self.fuzz_format_strings == True):
		self.TestCase2(0x00,0xff)

	if (self.fuzz_bit_flipping == True):
		self.TestCase3(0x00,0xff,14)


	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: CEC Fuzzer finished\n")

	self.fplog.write(time.strftime("%H:%M:%S  ", time.localtime()))
	self.fplog.write("Fuzzing: CEC Fuzzer finished\n")

	self.fuzzing = False
	self.statusbar.SetStatusText("Status: Normal", 3)
	self.fplog.close()


    def StopFuzzing(self,event):
	
	if (self.fuzzing == False):
		return

	self.fuzzing = False

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: Fuzzing stopped by user\n")

	self.fplog.write(time.strftime("%H:%M:%S  ", time.localtime()))
	self.fplog.write("Fuzzing: Fuzzing stopped by user\n")

	self.statusbar.SetStatusText("Status: Normal", 3)




	# -----------------------------------------------------------------------------
	# TestCase #1 - Long strings
	# -----------------------------------------------------------------------------
	
    def TestCase1(self, start, end):

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #1 - Long strings\n")

	self.fplog.write(time.strftime("%H:%M:%S  ", time.localtime()))
	self.fplog.write("Fuzzing: TestCase #1 - Long strings\n")
	
	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #1 - 14 bytes\n")
	string = "61 " * 14
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #1 - 15 bytes\n")
	string = "61 " * 15
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #1 - 100 bytes\n")
	string = "61 " * 100
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #1 - 300 bytes\n")
	string = "61 " * 300
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #1 - finished\n")


	# -----------------------------------------------------------------------------
	# TestCase #2 - Format strings
	# -----------------------------------------------------------------------------
	
    def TestCase2(self, start, end):

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Format strings\n")

	self.fplog.write(time.strftime("%H:%M:%S  ", time.localtime()))
	self.fplog.write("Fuzzing: TestCase #2 - Format strings\n")
	
	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #1\n")
	string = "25 6e 25 6e 25 6e 25 6e 25 6e" # %n%n%n%n%n
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #2\n")
	string = "25 70 25 70 25 70 25 70 25 70" # %p%p%p%p%p
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #3\n")
	string = "25 73 25 73 25 73 25 73 25 73" # %s%s%s%s%s
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #4\n")
	string = "25 78 25 78 25 78 25 78 25 78" # %x%x%x%x%x
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #5\n")
	string = "25 73 25 70 25 78 25 64" # %s%p%x%d
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #6\n")
	string = "25 2e 31 30 32 34 64" # %.1024d
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #7\n")
	string = "25 2e 31 30 32 35 64" # %.1025d
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #8\n")
	string = "25 2e 32 30 34 38 64" # %.2048d
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #9\n")
	string = "25 2e 32 30 34 39 64" # %.2049d
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #10\n")
	string = "25 2e 34 30 39 36 64" # %.4096d
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #11\n")
	string = "25 2e 34 30 39 37 64" # %.4097d
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #12\n")
	string = "25 39 39 39 39 39 39 39 39 39 39 73" # %9999999999s
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #13\n")
	string = "25 30 38 78" # %08x
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #14\n")
	string = "25 25 32 30 6e" # %%20n
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #15\n")
	string = "25 25 32 30 70" # %%20p
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #16\n")
	string = "25 25 32 30 73" # %%20s
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #17\n")
	string = "25 25 32 30 64" # %%20d
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - Test #18\n")
	string = "25 25 32 30 78" # %%20x
	self.TestType2(string,start,end)

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #2 - finished\n")



	# -----------------------------------------------------------------------------
	# TestCase #3 - Iterative bit flip
	# -----------------------------------------------------------------------------
	
    def TestCase3(self, start, end, maxparams):

	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #3 - Iterative bit flip\n")

	self.fplog.write(time.strftime("%H:%M:%S  ", time.localtime()))
	self.fplog.write("Fuzzing: TestCase #3 - Iterative bit flip\n")


	x = 0
	y = 0
	string = ""
	prev = ""

	while (x < maxparams and self.fuzzing == True):
		while (y < 256 and self.fuzzing == True):
			temp = "%02x" % y
			string = prev + temp.upper()
			self.TestType2(string,start,end)
			self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
			self.output.AppendText("Fuzzing: TestCase #3 - data = ")
			self.output.AppendText(string)
			self.output.AppendText("\n")
			y += 1
		prev += "FF "
		y = 0
		x += 1
		
	self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
	self.output.AppendText("Fuzzing: TestCase #3 - finished\n")




	# -----------------------------------------------------------------------------
	# TestType #1 - Iterate through all possible opcodes with no data
	# -----------------------------------------------------------------------------
	
    def TestType1(self):

	x = 0
	CommandSent = ""
	data = ""
	while (x < 256 and self.fuzzing == True):
		wx.Yield()

		if (x == 0x36):		# skip standby command
			x = 0x37

		opcode = "%02x" % x
		opcode = opcode.upper()
		CommandSent = self.SendCommand(self.target,opcode,data)
		print CommandSent

		self.fplog.write(time.strftime("%H:%M:%S  ", time.localtime()))
		self.fplog.write(CommandSent)
		self.fplog.write("\n")

		self.DisplayResponse()
		x+=1		


	# -----------------------------------------------------------------------------
	# TestType #2 - Send the same parameter bytes to a number of opcodes
	# -----------------------------------------------------------------------------

    def TestType2(self, parameter_bytes, start, end):
	
	x = start
	CommandSent = ""
	data = parameter_bytes
	while (x < end+1 and self.fuzzing == True):
		wx.Yield()

		if (x == 0x36):		# skip standby command
			x = 0x37

		opcode = "%02x" % x
		opcode = opcode.upper()
		CommandSent = self.SendCommand(self.target,opcode,data)
		print CommandSent

		self.fplog.write(time.strftime("%H:%M:%S  ", time.localtime()))
		self.fplog.write(CommandSent)
		self.fplog.write("\n")

		self.DisplayResponse()
		x+=1		
	


	# -----------------------------------------------------------------------------
	# TestType #3 - Mutate data then send with specific opcode
	# -----------------------------------------------------------------------------

    def TestType3(self, parameter_bytes_list, opcode, number_mutations):
	
	x = 0
	temp_list = []
	byte_to_mutate = 0
	mutate_value = 0
	data = ""
	number_of_bytes = len(parameter_bytes_list)
	number_of_bytes -= 1

	while (x < number_mutations and self.fuzzing == True):

		wx.Yield()
		
		temp_list = parameter_bytes_list

		print parameter_bytes_list
		print temp_list

		byte_to_mutate = randint(0,number_of_bytes)		
		temp_list[byte_to_mutate] = randint(0,255)

		y = 0
		while (y < number_of_bytes+1):
			data += "%02x " % temp_list[y]			
			y+=1

		data = data.upper()
		data = data[:-1]	#remove final space

		CommandSent = self.SendCommand(self.target,opcode,data)
		print CommandSent

		self.fplog.write(time.strftime("%H:%M:%S  ", time.localtime()))
		self.fplog.write(CommandSent)
		self.fplog.write("\n")

		self.DisplayResponse()
		
		data = ""
		x+=1




    def ReceiveData(self):
	buf = self.ser.read(1000)

	return buf


    def DisplayResponse(self):

	self.buf = self.ReceiveData()

	self.buf = string.replace(self.buf, "\r\n", "\n" )
	self.buf = string.replace(self.buf, "\r", "" )
	self.buf = string.replace(self.buf, "\n\n", "\n" )


	if (self.fuzzing == True):

		self.fplog.write(time.strftime("%H:%M:%S  ", time.localtime()))
		self.fplog.write(self.buf)


	if len(self.buf) > 1:
		print self.buf

	x = 0
	linebuf=""

	while (x < len (self.buf)):
		data=""	
		source=""
		dest=""
		opcode=""
	
		x+=1	# read "?"

		if (x+2 < len (self.buf) - 1):
			if (self.buf[x] == "S" and self.buf[x+1] == "T" and self.buf[x+2] == "A"):
				x+=6
				continue

		x+=4 	# read "REC "

		if (x < len (self.buf) - 1):
			source = self.buf[x]		# parse logical source address
		else:
			self.output.AppendText("\n")	
			break				# or leave

		x+=1	# source
		
		if (x < len (self.buf) - 1):
			dest = self.buf[x]		# parse logical source address
		else:
			self.output.AppendText("\n")
			break				# or leave

		x+=2	# dest + space

		# Parse data

		if (x < len (self.buf) - 1):
			while (self.buf[x] != "\n"):			
				data += self.buf[x]	# parse data			
				x+=1


		x+=1	# carriage return


		# Parse opcode

		if (len(data) > 2):
			opcode = data[0]
			opcode += data[1]
			data = data[3:]		# remove opcode from the data


		# At this point we should have parsed the data from a response like ?REC 04 47 54 56 1

		if (dest == self.target):

			status = data[-2:]			

			if (status == "2" or status == " 2"):
				if (self.capture == True):
					continue

				self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
				self.output.AppendText ("Error: No response from target!\n")
				continue


		if (dest == self.source or dest == "F" or self.capture == True):		# the filter - is it to us or to the broadcast address?

			data = data[:-2]	# remove status byte


			if (len(opcode) == 0):
				if (self.suppress_polling_messages == True):
					continue					#suppress "polling" messages

			self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
			self.output.AppendText("Source: ")
			self.output.AppendText(source)
			self.output.AppendText(" Dest: ")			
			self.output.AppendText(dest)
			self.output.AppendText(" ")			
			

			if (len(opcode) > 0):
				z = 0
				while (z < len (self.command_list)):
					if (self.command_list[z][1] == opcode):
						retcommand = self.command_list[z][0]
						self.output.AppendText("\"")
						self.output.AppendText(retcommand)
						self.output.AppendText("\" ")											
						break
					z+=1
			else:
				if (self.suppress_polling_messages == False): 
					self.output.AppendText("\"")	
					self.output.AppendText("polling")
					self.output.AppendText("\"")
					self.output.AppendText("\n")
					continue

			datalist = data.split(' ')

			#------- parse command-specific responses -------------------


			if opcode == "00" and len(datalist) > 1:	# Feature Abort

				print datalist
				if datalist[1] == "00":	
					self.output.AppendText("(Unrecognized opcode) ")
				if datalist[1] == "01":	
					self.output.AppendText("(Not in correct mode to respond) ")
				if datalist[1] == "02":	
					self.output.AppendText("(Cannot provide source) ")
				if datalist[1] == "03":	
					self.output.AppendText("(Invalid operand) ")
				if datalist[1] == "04":	
					self.output.AppendText("(Refused) ")
				if datalist[1] == "05":	
					self.output.AppendText("(Unable to determine) ")


			#------------------------------------------------------------

			if opcode == "47":	# OSD Name

				a = 0				

				self.output.AppendText("(")
				while (a < len(datalist)):

					if datalist[a] != "":				
						byte = int(datalist[a],16)
					else:
						a+=1
						continue

					if (byte > 31 and byte < 127):
						temp = "%c" % int(datalist[a],16)
						self.output.AppendText(temp)
					else:
						self.output.AppendText(".")
					a+=1
												
				self.output.AppendText(")")

				
 			#------------------------------------------------------------

			if opcode == "87":	# Vendor ID

				a = 0
				vendor_known = False
				while (a < len(self.vendorid_list)):
					if data == self.vendorid_list[a][1]:
						vendor = self.vendorid_list[a][0]
						self.output.AppendText("(")
						self.output.AppendText(vendor)
						self.output.AppendText(") ")
						vendor_known = True
					a+=1
						
				if vendor_known == False:
					self.output.AppendText("(")
					self.output.AppendText("Vendor unknown")	
					self.output.AppendText(") ")

			#------------------------------------------------------------

			if opcode == "9E":	# CEC Version

				if datalist[0] == "04":	
					self.output.AppendText("(HDMI v1.3a) ")
				if datalist[0] == "05":	
					self.output.AppendText("(HDMI v1.4 or v1.4a) ")

			if opcode == "90":	# Power Status

				if datalist[0] == "00":	
					self.output.AppendText("(On) ")
				if datalist[0] == "01":	
					self.output.AppendText("(Standby) ")
				if datalist[0] == "02":	
					self.output.AppendText("(Transition - standby to on) ")
				if datalist[0] == "03":	
					self.output.AppendText("(Transition - on to standby) ")

			#------------------------------------------------------------

			if opcode == "A0":	# Vendor command with ID

				vendortxt = data[:8] 

				a = 0
				vendor_known = False
				while (a < len(self.vendorid_list)):
					if vendortxt == self.vendorid_list[a][1]:
						vendor = self.vendorid_list[a][0]
						self.output.AppendText("(")
						self.output.AppendText(vendor)
						self.output.AppendText(") ")
						vendor_known = True
					a+=1
						
				if vendor_known == False:
					self.output.AppendText("(")
					self.output.AppendText("Vendor unknown")	
					self.output.AppendText(") ")

			#------------------------------------------------------------

			if self.dataview == False:
				self.output.AppendText("\n")
				continue		
			

			self.output.AppendText("Data: ")
			self.output.AppendText(data)			
						
			#if (len(datalist) != 1):
			self.output.AppendText(" ")

			y = 0				

			self.output.AppendText("\"")
			while (y < len(datalist)):
				if (len(datalist) == 1):					
					break

				if datalist[y] != "":				
					byte = int(datalist[y],16)
				else:
					y+=1
					continue

				if (byte > 31 and byte < 127):
					temp = "%c" % int(datalist[y],16)
					self.output.AppendText(temp)
				else:
					self.output.AppendText(".")
				y+=1
												
			self.output.AppendText("\"")
			self.output.AppendText("\n")
		



    def OnKey(self, evt): 
    # keycodes for arrow keys, page up/down, CR 
    	KEYS_TO_CANCEL = [314, 316, 366, 367, 13] 

    	keycode = evt.GetKeyCode()

	if keycode == 315:
		if (self.current_font_size < 20):
			self.current_font_size += 1
			f = wx.Font(self.current_font_size, wx.MODERN, wx.NORMAL, wx.NORMAL)
			self.output.SetDefaultStyle(wx.TextAttr("GREEN", wx.NullColour, f))
			self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
			self.output.AppendText("Status: Font size increased\n")
			return


	if keycode == 317:
		if (self.current_font_size > 8):
			self.current_font_size -= 1
			f = wx.Font(self.current_font_size, wx.MODERN, wx.NORMAL, wx.NORMAL)
			self.output.SetDefaultStyle(wx.TextAttr("GREEN", wx.NullColour, f))
			self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
			self.output.AppendText("Status: Font size decreased\n")
			return


	if keycode == 27:
		self.command.AppendText("\nCEC:> ")
		self.commandmode = False
		self.cdc_commandmode = False


	if keycode in KEYS_TO_CANCEL: 
		if keycode == 13:

			#--------------- Is a CEC or CDC command selected? Or has anything been typed? ------


			if ((self.commandmode == False) and (self.cdc_commandmode == False) and len(self.inputbufferlist) == 0):		
				self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
				self.output.AppendText("Error: Command not selected!\n")
				return


			#--------------- Is there a CR present that should be removed? ----------------------

			if len(self.inputbufferlist) > 0:
				if (self.inputbufferlist[0] == 13):	# remove CR if present
					self.inputbufferlist.pop(0)


			#--------------- Has a CEC command been typed? --------------------------------------

			if (self.commandmode == False and self.cdc_commandmode == False and len(self.inputbufferlist) > 0):				
				x=0
				self.opcode = ""
				while (x<2):
					self.opcode += "%c" % self.inputbufferlist[x]
					x+=1 
				self.inputbufferlist.pop(0)	# remove opcode + space from data
				self.inputbufferlist.pop(0)				
		
			#--------------- Are parameters required, but have not been supplied? ---------------

			if ((len(self.inputbufferlist) == 0 or len(self.inputbufferlist) == 1) and (self.parameters_required == 1 or self.cdc_parameters_required == 1)):
				self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
				self.output.AppendText("Error: Command requires parameters!\n")
				return

			#--------------- Is this a CDC command? ---------------------------------------------

			if (self.cdc_commandmode == True):
				self.opcode = "F8"
				self.command_data = self.physical[:2]	#first byte of physical address
				self.command_data += " " 
				self.command_data += self.physical[-2:]	#second byte of physical address
				self.command_data += " "
				self.command_data += self.cdc_opcode
				self.command_data += " "

			x=0

			if len(self.inputbufferlist) > 0:
				if (self.inputbufferlist[0] == 32):
					self.inputbufferlist.pop(0)

			while (x<len(self.inputbufferlist)):			

				self.command_data += "%c" % self.inputbufferlist[x]
				x+=1 

			self.SendCommand(self.target,self.opcode,self.command_data)

			self.command_data = ""
			self.opcode = ""
			self.cdc_opcode = ""
			self.inputbufferlist = []
					
			self.DisplayResponse()
			
			self.command.AppendText("\nCEC:> ")
			self.parameters_required = 0
			self.cdc_parameters_required = 0
			self.commandmode = False
			self.cdc_commandmode = False
			
    	else: 
        	evt.Skip() 

	if keycode == 8:			#delete key
		self.inputbufferlist.pop()
		if (len(self.inputbufferlist) < 1):
			self.commandmode == False
		return

	self.inputbufferlist.append(keycode)
	#print self.inputbufferlist

	


    def ProcessCommand(self, event):
	item = self.parent.GetMenuBar().FindItemById(event.GetId())
        selected = item.GetText()

	x = 0
	while (x < len (self.command_list)):
		if (self.command_list[x][0] == selected):
			self.opcode = self.command_list[x][1]
			self.parameters_required = self.command_list[x][2]
			self.command.AppendText("\nCEC:")
			self.command.AppendText(self.command_list[x][0])
			self.command.AppendText(">")
			self.CurrentCommand = self.command_list[x][0]
			self.commandmode = True
		x+=1



    def ProcessCDCCommand(self, event):
	item = self.parent.GetMenuBar().FindItemById(event.GetId())
        selected = item.GetText()

	x = 0
	while (x < len (self.cdc_command_list)):
		if (self.cdc_command_list[x][0] == selected):
			self.cdc_opcode = self.cdc_command_list[x][1]
			self.cdc_parameters_required = self.cdc_command_list[x][2]
			self.command.AppendText("\nCDC:")
			self.command.AppendText(self.cdc_command_list[x][0])
			self.command.AppendText(">")
			self.CurrentCommand = self.cdc_command_list[x][0]
			self.cdc_commandmode = True			
		x+=1


    def ProcessSourceSelect(self, event):
	item = self.parent.GetMenuBar().FindItemById(event.GetId())
        selected = item.GetText()
	print selected
	x = 0
	while (x < len (self.source_list)):
		if (self.source_list[x][0] == selected):
			self.source = self.source_list[x][1]
			command = "!A " + self.source + "~"
			self.RawCommandSend (command)
			self.sourcename = self.source_list[x][0]			
			status1 = "Source Device: " + self.sourcename
			status2 = "Target Device: " + self.targetname
       			self.statusbar.SetStatusText(status1, 1) 
			self.statusbar.SetStatusText(status2, 2)
			self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
			self.output.AppendText("Status: Source changed to \"")
			self.output.AppendText(self.sourcename)
			self.output.AppendText("\"\n")
			
		x+=1



    def ProcessTargetSelect(self, event):
	item = self.parent.GetMenuBar().FindItemById(event.GetId())
        selected = item.GetText()

	x = 0
	while (x < len (self.target_list)):
		if (self.target_list[x][0] == selected):
			self.target = self.target_list[x][1]
			self.targetname = self.target_list[x][0]			
			status1 = "Source Device: " + self.sourcename
			status2 = "Target Device: " + self.targetname
       			self.statusbar.SetStatusText(status1, 1) 
			self.statusbar.SetStatusText(status2, 2)
			self.output.AppendText(time.strftime("%H:%M:%S  ", time.localtime()))
			self.output.AppendText("Status: Target changed to \"")
			self.output.AppendText(self.target_list[x][0])
			self.output.AppendText("\"\n")
			
		x+=1

   
    def About(self, event):
        wx.MessageBox("CECSTeR v1.0: Andy Davis, NCC Group 2012", caption="Information", style=wx.OK|wx.ICON_INFORMATION, parent=self)
        return(1)
        
    def CloseMe(self, event):
        self.parent.Close(True)


app = wx.App(False)  
frame = wx.Frame(None, wx.ID_ANY, "CECSTeR", size=(1024,768)) 

win = MainPanel(frame)
frame.Show(True) 
frame.Center()   
app.MainLoop()
