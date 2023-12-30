import { useParams } from "react-router-dom";
import { urls } from "../../utils/data";
import GrafanaPanel from "../../components/shared/grafana/GrafanaPanel/GrafanaPanel";
import { StyledPage } from "../../components/shared/styled/SharedStyles.styled";

export default function DeviceDetailsPage() {
    const { deviceId } = useParams();

    const dashboard = urls.find(item => item.type === deviceId);
    const dashboardUrl = dashboard ? dashboard.url : null;

    return (
        <StyledPage>
            <h2>Dashboard for Device Type: {deviceId}</h2>
            {dashboardUrl ? (
                <GrafanaPanel url={dashboardUrl} />
            ) : (
                <p>No dashboard available for this device type.</p>
            )}
        </StyledPage>
    );
}