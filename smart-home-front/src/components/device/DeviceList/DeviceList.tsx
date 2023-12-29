import { Device } from "../../../models/Device"
import DeviceCard from "../DeviceCard/DeviceCard";
import { ItemsListStyle } from "./DeviceList.styled";

export type DeviceListProps = {
    devices : Device[];
    onDetails : (device : Device) => void;

}

export default function DeviceList({devices, onDetails} : DeviceListProps){
    const seenTypes = new Set();

    const filteredDevices = devices.filter(device => {
        if (!seenTypes.has(device.type)) {
            seenTypes.add(device.type);
            return true;
        }
        return false;
    });

    return (
        <ItemsListStyle>
            {filteredDevices.map(device => (
                <DeviceCard 
                    key={device.type} 
                    device={device} 
                    onDetails={() => onDetails(device)} 
                />
            ))}
        </ItemsListStyle>
    );
}