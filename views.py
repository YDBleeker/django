from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
import platform

@require_http_methods(["GET"])
def get_wifi_networks(request):

    wifi_networks = []

    try:
        # Detect the platform
        current_platform = platform.system()

        if current_platform == "Linux":
            # Run a command to list Wi-Fi networks on Linux (Raspberry Pi)
            result = subprocess.run(["iwlist", "wlan0", "scan"], capture_output=True, text=True)
            output = result.stdout

            # Parse the output to extract Wi-Fi network information
            for line in output.split('\n'):
                if "ESSID" in line:
                    ssid = line.split('ESSID:"')[1].split('"')[0]
                    wifi_networks.append({"ssid": ssid})

        elif current_platform == "Windows":
            # Run a command to list Wi-Fi networks on Windows
            result = subprocess.run(["netsh", "wlan", "show", "networks"], capture_output=True, text=True)
            output = result.stdout

            # Parse the output to extract Wi-Fi network SSIDs
            lines = output.split('\n')
            ssid_lines = [line.split(":")[1].strip() for line in lines if line.strip().startswith("SSID")]
            wifi_networks.extend({"ssid": ssid} for ssid in ssid_lines)
            
        else:
            # Handle other platforms if needed
            return JsonResponse({"error": "Unsupported platform"})

    except Exception as e:
        # Handle exceptions if the command fails
        return JsonResponse({"error": str(e)})

    print("wifi_networks")
    print(wifi_networks)
    return JsonResponse({"wifi_networks": wifi_networks})

@require_http_methods(["GET"])
def reboot(request):
    try:
        if platform.system() == 'Windows':
            subprocess.run(['shutdown', '/r', '/t', '1'], check=True)
        elif platform.system() == 'Linux':
            subprocess.run(['sudo', 'reboot'], check=True)
        else:
            raise NotImplementedError(f"Reboot not supported on {platform.system()}")

        response_data = {'success': True, 'message': 'Reboot initiated.'}
        return JsonResponse(response_data)
    except Exception as e:
        response_data = {'success': False, 'message': str(e)}
        return JsonResponse(response_data, status=500)

@require_http_methods(["GET"])
def emotion(request):
    # get emotion from mqtt and cms here
    emotion = "happy"
    return JsonResponse({"emotion": emotion})

@csrf_exempt
@require_http_methods(["POST"])
def connect_to_wifi(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        ssid = data.get("ssid")
        password = data.get("password")

        # Detect the platform
        current_platform = platform.system()

        if current_platform == "Linux":
            # Run a command to connect to Wi-Fi on Linux (Raspberry Pi)
            subprocess.run(["sudo", "nmcli", "dev", "wifi", "connect", ssid, "password", password], check=True)

        elif current_platform == "Windows":
            # Add the Wi-Fi network profile
            try:
                # Create the command to connect to WiFi using netsh
                command = f'netsh wlan connect name="{ssid}" ssid="{ssid}"'

                 # Run the command using subprocess
                subprocess.run(command, check=True, shell=True)

                # If the command was successful, attempt to enter the password
                if password:
                    command = f'netsh wlan set profileparameter name="{ssid}" keyMaterial="{password}"'
                    subprocess.run(command, check=True, shell=True)

                print(f"Connected to WiFi network: {ssid}")

            except subprocess.CalledProcessError as e:
                print(f"Error connecting to WiFi network: {ssid}")
                print(f"Error details: {e}")
         
        else:
            # Handle other platforms if needed
            return JsonResponse({"error": "Unsupported platform"})

        return JsonResponse({"message": f"Successfully connected to Wi-Fi network: {ssid}"})
    
    except json.JSONDecodeError as e:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except subprocess.CalledProcessError as e:
        return JsonResponse({"error": f"Failed to connect to Wi-Fi: {str(e)}"}, status=500)


def helloworld(request):
    return JsonResponse({'message': 'Hello, World!'})

def index(request):
    return render(request, 'index.html')

def wifi(request):
    return render(request, 'wifi.html')

def setting(request):
    return render(request, 'settings.html')

def uuid(request):
    context = {'uuid': 'd3f5071c-8def-11ee-b9d1-0242ac120002'}
    return render(request, 'uuid.html', context)
