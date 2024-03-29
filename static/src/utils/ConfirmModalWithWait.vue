<template>
  <empty-modal :no-close="noClose">
    <form id="modalform">
      <div class="modal-header border-bottom-0">
        <div id="modal_with_wait_title" class="modal-title">{{ title }}</div>
        <button v-if="!noClose"
                type="button"
                class="close"
                data-dismiss="modal"
                aria-label="Fermer"
                @click="closeModal">
                <span class="sr-only">Fermer</span>
        </button>
      </div>
      <div class="modal-body">
        <error-bar v-if="errorMessage">
          <p>{{ errorMessage }}</p>
        </error-bar>
        <slot></slot>
      </div>
      <div class="modal-footer border-top-0">
        <button v-if="confirmButton" type="submit" class="btn btn-primary"
                @click="confirmClicked"
                :class="{'btn-loading': processing}"
        >
          {{ confirmButton }}
        </button>
        <button v-if="cancelButton" type="button" class="btn btn-secondary"
                data-dismiss="modal"
                @click="cancelClicked"
        >
          {{ cancelButton }}
        </button>
      </div>
    </form>
  </empty-modal>
</template>

<script>
import EmptyModal from "./EmptyModal";
import ErrorBar from "./ErrorBar";
import reportValidity from "report-validity";
import Vue from "vue";

export default Vue.extend({
  props: [
    "cancel-button",
    "confirm-button",
    "no-close",
    "title",
    "submitCallback",
    "errorCallback",
    "successCallback",
  ],
  data: function() {
    return {
      errorMessage: "",
      processing: false,
    };
  },
  components: {
    EmptyModal,
    ErrorBar,
  },
  methods: {
    confirmClicked () {
      // Disabling submit behaviour for Firefox
      document.getElementById("modalform").addEventListener(
        "submit",
        function(event){event.preventDefault();}
      );

      this.errorMessage = "";
      if (!this.validateForm()) {
        return;
      }

      const processingDoneCallback = (errorMessage, successMessage, refreshUrl) => {
        if (errorMessage) {
          console.log("error!", errorMessage);
          this.errorMessage = errorMessage;
          this.processing = false;
          return;
        }
        console.debug("ConfirmModalWithWait : processing done", successMessage);
        if (refreshUrl) {
          window.location.href = refreshUrl;
        }
      };

      this.processing = true;
      this.$emit("confirm", processingDoneCallback);
    },
    cancelClicked () {
      this.processing = false;
      this.errorMessage = "";
      this.$emit("cancel");
    },
    closeModal () {
      this.processing = false;
      this.errorMessage = "";
      this.$emit("close");
    },
    validateForm () {
      const forms = this.$el.getElementsByTagName("form");
      if (forms.length > 0) {
        return reportValidity(forms[0]);
      }
      return true;
    },
  },
});
</script>
