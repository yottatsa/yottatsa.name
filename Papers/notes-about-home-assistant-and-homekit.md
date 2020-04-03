# Notes about Home Assistant and HomeKit
<time datetime="2018-04-01"/>

Well, it's complicated. I run bunch of outdated hardware, and it is not working as smooth as I expected from Apple. So either I need to upgrade, or I have to research and hack a bit.

The [3rd generation of Apple TV has no CEC support](https://www.quora.com/Does-the-Apple-TV-3rd-gen-support-HDMI-CEC-a-k-a-HDMI-Control). So I need to read it's status to power on the TV automatically.

Also, the TV has Youtube app, but it couldn't switch the TV on. So it's useful to have a HomeKit Switch to turn it on, and then switch it off with Siri.

## My setup

* *Philips Ambilight TV 50PUS6272/05*. It runs webOS with jointSPACE v6, which is controlled best with both API and CEC.
* *Apple TV*, 3rd generation.
* *Raspberry Pi 3 B+*. It runs Home Assistant with [`hdmi_cec`][hdmi_cec], [`philips_js`][philips_js], [`apple_tv`][apple_tv], and [`homekit`][homekit] components to automate them.
* Lots of Apple devices. HomeKit is shared amongst a laptop and a phone, and a partner of mine.

## Issues

[3rd generation of Apple TV is limited in it's HomeKit support](https://support.apple.com/en-gb/HT207057). It allows to contol HomeKit accessories remotely, but doesn't support it for shared users. It enables automatically when you log into your iCloud account on the Apple TV. However, for some reason, only Hue brigde is working over multiple devices. Home Assistant accessories are only working on a master device, other devices fails with *No response*.

Also, I found that Apple TV remote credentials expires every time if the iCloud is enabled on the Apple TV.

## Conclusion

So the easiest way to make everything works stable is not to use iCloud with an old Apple TV.

Otherwise, it could be upgraded to the lasest generation, which is advertised with much better HomeKit support, and also supports CEC.

[hdmi_cec]: <https://www.home-assistant.io/components/hdmi_cec/>
[philips_js]: <https://www.home-assistant.io/components/media_player.philips_js/>
[apple_tv]: <https://www.home-assistant.io/components/apple_tv/>
[homekit]: <https://www.home-assistant.io/components/homekit/>
