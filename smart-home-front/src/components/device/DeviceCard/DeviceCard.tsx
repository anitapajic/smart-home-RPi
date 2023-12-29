import { Device } from "../../../models/Device";
import { Card } from "./DeviceCard.styled";

export type DeviceCardProps = {
    device: Device;
    onDetails?: (device: Device) => void;
}

export default function DeviceCard({ device, onDetails }: DeviceCardProps) {
    const handleOnDetails = () => {
        if (onDetails) {
            onDetails(device);
        }
    }
    return (
        <Card onClick={handleOnDetails}>
            <h3>{device.type}</h3>
        </Card>
    );
}