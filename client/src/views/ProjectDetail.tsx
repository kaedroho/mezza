import { Form, NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import { Tab, TabList, TabPanel, Tabs } from "@mui/joy";
import Button from "@mui/joy/Button";
import React from "react";
import AssetList from "../components/AssetList";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { CSRFTokenContext } from "../contexts";
import FormDef from "../deserializers/Form";
import { Asset, Project } from "../types";

interface ProjectDetailViewProps {
  project: Project;
  basicInfoForm: FormDef;
  assets: Asset[];
}

export default function ProjectDetailView({
  project,
  basicInfoForm,
  assets,
}: ProjectDetailViewProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);
  const csrfToken = React.useContext(CSRFTokenContext);

  return (
    <Layout title={project.title} noIndent>
      <Tabs defaultValue={0}>
        <TabList>
          <Tab>Basic Information</Tab>
          <Tab>Script</Tab>
          <Tab>Assets</Tab>
        </TabList>
        <TabPanel value={0}>
          <Form action={project.detail_url} method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />

            {basicInfoForm.render()}

            <Button color="primary" type="submit">
              Save
            </Button>
          </Form>
        </TabPanel>
        <TabPanel value={1}></TabPanel>
        <TabPanel value={2}>
          <Button
            variant="plain"
            color="primary"
            size="sm"
            startDecorator={<Add />}
            onClick={() =>
              openOverlay(
                project.asset_upload_url,
                (content) => (
                  <ModalWindow slideout="right">{content}</ModalWindow>
                ),
                {
                  onClose: () => {
                    // Refresh props so new post pops up in listing
                    refreshProps();
                  },
                },
              )
            }
          >
            Upload
          </Button>
          <AssetList assets={assets} />
        </TabPanel>
      </Tabs>
    </Layout>
  );
}
