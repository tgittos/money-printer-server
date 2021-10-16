import styles from "../Header.module.scss";
import {MdNotificationsNone, MdNotificationsActive} from "react-icons/all";
import {Badge} from "react-bootstrap";

export interface INotificationsBadgeProps {
    className?: string;
    notificationCount: number;
}

const NotificationsBadge = (props: INotificationsBadgeProps) => {
    const classes = [
        props.className ?? '',
        styles.NotificationsBadge,
        'mp-notifications-badge',
    ];

    return <div className={classes.join(' ')}>
        { props.notificationCount > 0
            ? <MdNotificationsActive />
            : <MdNotificationsNone/>
        }
        {props.notificationCount > 0
            ? <Badge bg="info" className="mp-badge-count">
                {props.notificationCount}
            </Badge>
            : <></>
        }
    </div>;
}

export default NotificationsBadge;
