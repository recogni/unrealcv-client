# unrealcv-client

A Recogni Inc specific version of a UnrealCV python client

## Usage:

```
./client.py --server 127.0.0.1 --port 9000
```

## Why

This is a simple python client that creates a AF_INET socket to a running UnrealCV plugin instance hosted on an accessible server.  Currently the allowed command-set are limited to all the normal UnrealCV commands.  The eventual goal of this client is to provide an easy way to script access into the UnrealEngine to facilitate model manipulation, injection, scene editing, camera movement and ultimately scene and object data capture.

It is expected that by the time all the above features are fully realized, we probably will migrate away from UnrealCV and move to our own plugin suited better for our needs and implementation.  However, in the interest of time and proving a point, this project exists as a temporary bridge.

## UnrealCV payload

```
4 bytes magic number
4 bytes payload size
n bytes payload where formatting is:
    "%d:%s" % (request_id, remote_command)
```

## How it works

Once the client is connected, you will get a REPL into the UnrealEngine's command console (to which some UnrealCV commands have been added).  The client will maintain an auto-incremented request id for each request that it sends to the socket as part of the UnrealCV TCP protocol.  Each response from the socket is printed out to standard out as it is seen from the server.

## Current commands

Here is a list of commands that you can get by querying `vget /unrealcv/help`:
```
vrun [str]
Run UE4 built-in commands
vget /objects
Get the name of all objects
vget /object/[str]/color
Get the labeling color of an object (used in object instance mask)
vset /object/[str]/color [uint] [uint] [uint]
Set the labeling color of an object [r, g, b]
vget /object/[str]/name
[debug] Get the object name
vget /object/[str]/location
Get object location [x, y, z]
vget /object/[str]/rotation
Get object rotation [pitch, yaw, roll]
vset /object/[str]/location [float] [float] [float]
Set object location [x, y, z]
vset /object/[str]/rotation [float] [float] [float]
Set object rotation [pitch, yaw, roll]
vget /camera/[uint]/[str]
Get snapshot from camera, the third parameter is optional
vget /camera/[uint]/[str] [str]
Get snapshot from camera, the third parameter is optional
vget /camera/[uint]/lit
Get snapshot from camera, the third parameter is optional
vget /camera/[uint]/lit [str]
Get snapshot from camera, the third parameter is optional
vget /camera/[uint]/object_mask
Get snapshot from camera, the third parameter is optional
vget /camera/[uint]/object_mask [str]
Get object mask from camera
vget /camera/[uint]/screenshot
Get snapshot from camera
vget /camera/[uint]/location
Get camera location [x, y, z]
vget /camera/[uint]/rotation
Get camera rotation [pitch, yaw, roll]
vset /camera/[uint]/location [float] [float] [float]
Teleport camera to location [x, y, z]
vset /camera/[uint]/moveto [float] [float] [float]
Move camera to location [x, y, z], will be blocked by objects
vset /camera/[uint]/rotation [float] [float] [float]
Set rotation [pitch, yaw, roll] of camera [id]
vget /camera/[uint]/proj_matrix
Get projection matrix from camera [id]
vset /viewmode [str]
Set ViewMode to (lit, normal, depth, object_mask)
vget /viewmode
Get current ViewMode
vget /actor/location
Get actor location [x, y, z]
vget /actor/rotation
Get actor rotation [pitch, yaw, roll]
vget /camera/[uint]/lit png
Return raw binary image data, instead of the image filename
vget /camera/[uint]/depth png
Return raw binary image data, instead of the image filename
vget /camera/[uint]/normal png
Return raw binary image data, instead of the image filename
vget /camera/[uint]/depth npy
Return raw binary image data, instead of the image filename
vget /unrealcv/status
Get the status of UnrealCV plugin
vget /unrealcv/help
List all available commands and their help message
vget /unrealcv/echo [str]
[debug] Echo back all message, for debug
vget /unrealcv/version
Get the version of UnrealCV, the format is v0.*.*
vget /scene/name
Get the name of this scene, to make sure the annotation data is for this scene.
vset /action/game/pause
Pause the game
vset /action/eyes_distance [float]
Set the distance of binocular stereo camera
vset /action/keyboard [str] [float]
Send a keyboard action to the game
vrun [str] [str]
Run UE4 built-in commands
vrun [str] [str] [str]
Run UE4 built-in commands
vexec [str] [str]
Run UE4 blueprint function
vexec [str] [str] [str]
Run UE4 blueprint function
vexec [str] [str] [str] [str]
Run UE4 blueprint function
vexec [str] [str] [str] [str] [str]
Run UE4 blueprint function
```
