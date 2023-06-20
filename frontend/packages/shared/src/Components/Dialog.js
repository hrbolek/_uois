import Button from "react-bootstrap/Button"
import Card from "react-bootstrap/Card"
import Modal from 'react-bootstrap/Modal';
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import { DatePicker } from "../.."
import { XLg } from "react-bootstrap-icons"

export const Dialog = ({children, size="xl", title="Dialog", oklabel="Ok", cancellabel="Zrušit", onOk, onCancel}) => {
    const onFinish = () => {
        if (onOk) {
            onOk()
        }
    }
    const onCancel_ = () => {
        if (onCancel) {
            onCancel()
        }
    }
    return (
        // <div className="modal show" style={{ display: 'block', position: 'initial' }} >
        <Modal size="xl" show={"true"} onHide={onCancel_}>
            <Modal.Header closeButton>
                <Modal.Title>{title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {children}
            </Modal.Body>
            <Modal.Footer>
                <Row>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Button variant="outline-success" onClick={onFinish}>{oklabel}</Button> &nbsp;
                            <Button variant="outline-danger" onClick={onCancel_}>{cancellabel}</Button>
                        </div>               
                    </Col>
                </Row>
            </Modal.Footer>
        </Modal>
        // </div>
    )
}