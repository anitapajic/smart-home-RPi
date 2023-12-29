import { useNavigate } from "react-router-dom";
import DeviceList from "../../components/device/DeviceList/DeviceList";
import { StyledPage } from "../../components/shared/styled/SharedStyles.styled";
import { devices } from "../../utils/data";
import { Device } from "../../models/Device";

export default function DevicesPage() {
    const navigate = useNavigate();

    const handleDetails = (device: Device) => {
        navigate(`/devices/${device.type}`)
    };

    return (
        <StyledPage>
            <h2>Devices Types</h2>
            <DeviceList 
            devices={devices}
            onDetails={handleDetails}/>
        </StyledPage>
    )
}